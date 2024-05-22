import React, { useEffect, useState } from "react";

function Modal({ source }) {
  const [open, setOpen] = useState(false);
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [inputValues, setInputValues] = useState({
     Window_Size: '3', 
      Mean:  '0',
      Standerd_deviation: '20', 
      K_value:  '1' ,
      Sigma: '1', 
      Level: '0',
      type:  '2',
      Resize: '0'
  });

  useEffect(() => {
    if (source) {
      setOpen(true);
      resetImage();
    }
  }, [source]);

  const handleClose = () => {
    setOpen(false);
    resetImage();
  };

  const resetImage = () => {
    setImageUrl('');
    setLoading(false);
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setInputValues({
      ...inputValues,
      [name]: value
    });
  };

  

  const handleFetchImage = async () => {

    setLoading(true);
    setImageUrl(''); // Clear previous image

 
    const valuesToSend = {
      ...inputValues,
      Window_Size: inputValues.Window_Size || '3', 
      Mean: inputValues.Mean || '0',
      Standerd_deviation: inputValues.Standerd_deviation || '20', 
      K_value: inputValues.K_value || '1' ,
      Sigma: inputValues.Sigma || '1', 
      Level: inputValues.Level || '0',
      type: inputValues.type || '2',
      Resize: inputValues.Resize || '0' ,
      salt: inputValues.salt || '0.05' ,
      pepper: inputValues.pepper || '0.05', 
      modet: inputValues.modet
      
    };

    console.log("Sending request with values:", valuesToSend);

    try {
      const response = await fetch(`http://127.0.0.1:5000/filters/${source}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(valuesToSend)
      });
      console.log("Response status:", response.status);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setImageUrl(url);
    } catch (error) {
      console.error('Error fetching the image:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderInputs = () => {
    switch (source) {
      case 'Median':
      case 'Averaging':
      case 'Adaptive':
        return (
          <>
            <label>
              Window Size:
              <input
                type="text"
                name="Window_Size"
                value={inputValues.Window_Size}
                onChange={handleInputChange}
              />
            </label>
          </>
        );
      case 'Gaussian_noise':
        return (
          <>
            <label>
              Standerd deviation:
              <input
                type="text"
                name="Standerd_deviation"
                value={inputValues.Standerd_deviation}
                onChange={handleInputChange}
              />
            </label>
            <label>
              Mean:
              <input
                type="text"
                name="Mean"
                value={inputValues.Mean}
                onChange={handleInputChange}
              />
            </label>
          </>
        );

      case 'Gaussian':
        return (
          <>
            <label>
              Window Size:
              <input
                type="text"
                name="Window_Size"
                value={inputValues.Window_Size}
                onChange={handleInputChange}
              />
            </label>
            <label>
              Sigma:
              <input
                type="text"
                name="Sigma"
                value={inputValues.Sigma}
                onChange={handleInputChange}
              />
            </label>
          </>
        );
      case 'Uniform_noise':
        return (
          <>
            <label>
              Level:
              <input
                type="text"
                name="Level"
                value={inputValues.Level}
                onChange={handleInputChange}
              />
            </label>
          </>
        );
        
      case 'Unsharp_Masking_and_Highboost':
        return (
          <>
            <label>
              K-value:
              <input
                type="number"
                name="K_value"
                value={inputValues.K_value}
                onChange={handleInputChange}
              />
            </label>
            
          </>
        );

      case 'Impulse_noise':
        return (
          <>
            <label>
              salt:
              <input
                type="text"
                name="salt"
                value={inputValues.salt}
                onChange={handleInputChange}
              />
            </label>
            
            <label>
              pepper:
              <input
                type="text"
                name="pepper"
                value={inputValues.pepper}
                onChange={handleInputChange}
              />
            </label>
            
          </>
        );
      
      case 'Interpolation':
        return (
          <>
            <label>
              Resize:
              <input
                type="test"
                name="Resize"
                value={inputValues.Resize}
                onChange={handleInputChange}
              />
            </label>

            <label>
              Type:
              <select
                name="type"
                value={inputValues.type}
                onChange={handleInputChange}
              >
                <option value="nearest_neighbor">nearest_neighbor</option>
                <option value="bilinear">bilinear</option>
              </select>
            </label>
            
          </>
        );

      
      case 'sobya':
        return (
          <>
            <label>
              mode:
              <select
                name="modet"
                value={inputValues.modet}
                onChange={handleInputChange}
              >
                <option value="mask">mask</option>
                <option value="mask_image">mask+image</option>
              </select>
            </label>
            
          </>
        );

      case 'Laplacian':
        return (
          <>
            <label>
              mode:
              <select
                name="modet"
                value={inputValues.modet}
                onChange={handleInputChange}
              >
                <option value="mask">mask</option>
                <option value="mask_image">mask+image</option>
              </select>
            </label>
            
          </>
        );
      case 'Roberts_Cross_Gradient':
        return (
          <>
            <label>
              mode:
              <select
                name="modet"
                value={inputValues.modet}
                onChange={handleInputChange}
              >
                <option value="mask">mask</option>
                <option value="mask_image">mask+image</option>
              </select>
            </label>
            
          </>
        );
      default:
        return null;
    }
  };

  if (!open) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button onClick={handleClose} className="close-button">X</button>
        {renderInputs()}
        <button onClick={handleFetchImage} className="submit-button">Submit</button>
        {loading ? (
          <div className="loading-icon">Loading...</div> // Replace with an actual loading spinner/icon if needed
        ) : (
          imageUrl && (
            <>
              <img src={imageUrl} alt="Fetched content" className="image" />
              <a href={imageUrl} download="image.jpg" className="download-button">
                Download
              </a>
            </>
          )
        )}
      </div>
    </div>
  );
}

export default Modal;
