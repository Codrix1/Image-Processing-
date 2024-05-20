import React, { useEffect, useState } from "react";

function Modal({ source }) {
  const [open, setOpen] = useState(false);
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [inputValues, setInputValues] = useState({
    Window_Size: '3', // Default value for Window_Size
    option1: '',
    option2: ''
  });
  const [errors, setErrors] = useState({}); // State to manage validation errors

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

  const validateInputs = () => {
    const newErrors = {};
    Object.keys(inputValues).forEach((key) => {
      if (!/^\d*$/.test(inputValues[key])) {
        newErrors[key] = 'This field must be a number';
      }
    });
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleFetchImage = async () => {
    if (!validateInputs()) return;

    setLoading(true);
    setImageUrl(''); // Clear previous image

 
    const valuesToSend = {
      ...inputValues,
      Window_Size: inputValues.Window_Size || '3', 
      Mean: inputValues.Mean || '0',
      Standerd_deviation: inputValues.Standerd_deviation || '20', 
      K_value: inputValues.K_value || '1' 

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
                type="number"
                name="Window_Size"
                value={inputValues.Window_Size}
                onChange={handleInputChange}
              />
              {errors.Window_Size && <span className="error-message">{errors.Window_Size}</span>}
            </label>
          </>
        );
      case 'Gaussian_noise':
        return (
          <>
            <label>
              Standerd deviation:
              <input
                type="number"
                name="Standerd_deviation"
                value={inputValues.Standerd_deviation}
                onChange={handleInputChange}
                min="1"
                max="150"
              />
              {errors.Standerd_deviation && <span className="error-message">{errors.Standerd_deviation}</span>}
            </label>
            <label>
              Mean:
              <input
                type="number"
                name="Mean"
                value={inputValues.Mean}
                onChange={handleInputChange}
                min="0"
                max ="20"
              />
              {errors.Mean && <span className="error-message">{errors.Mean}</span>}
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
              {errors.K_value && <span className="error-message">{errors.K_value}</span>}
            </label>
          </>
        );
      case 'filter2':
        return (
          <>
            <label>
              Option 1:
              <select
                name="option1"
                value={inputValues.option1}
                onChange={handleInputChange}
              >
                <option value="">Select an option</option>
                <option value="optionA">Option A</option>
                <option value="optionB">Option B</option>
              </select>
              {errors.option1 && <span className="error-message">{errors.option1}</span>}
            </label>
            <label>
              Option 2:
              <select
                name="option2"
                value={inputValues.option2}
                onChange={handleInputChange}
              >
                <option value="">Select an option</option>
                <option value="optionC">Option C</option>
                <option value="optionD">Option D</option>
              </select>
              {errors.option2 && <span className="error-message">{errors.option2}</span>}
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
