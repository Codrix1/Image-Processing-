import React, { useEffect, useRef } from "react";
import { useState } from "react";

const Matching_upload = () => {

    const [selectedFile, setSelectedFile] = useState(null);
    const [message, setMessage] = useState('');
    const [imageUrl, setImageUrl] = useState(null);
    const fileInputRef = useRef(null);

    useEffect(() => {
        fetchImage();
    }, []);

    const fetchImage = () => {
        fetch('http://127.0.0.1:5000/get/reference')
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                setImageUrl(url);
            })
            .catch(error => {
                setMessage('Failed to load image');
            });
    };

    const onFileChange = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
        setMessage(''); // Clear message when a new file is selected

        if (file) {
            onFileUpload(file);
        }
    };

    const onFileUpload = (file) => {
        const formData = new FormData();
        formData.append('file', file);

        fetch('http://127.0.0.1:5000/upload/reference', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                setMessage(data.success);
                fetchImage(); // Refresh the image
            } else {
                setMessage(data.error || 'File upload failed');
            }
        })
        .catch(error => {
            setMessage('File upload failed');
        })
        .finally(() => {
            setSelectedFile(null); // Clear the selected file state to allow new uploads
            fileInputRef.current.value = ''; // Reset the file input value to allow selecting the same file again
        });
    };

  

    const onButtonClick = () => {
        fileInputRef.current.click();
    };

    return (
        <div>
            <div className="main_Container_image">

            <div className="image-container">
                <h3 className="Center">Reference Image</h3>
                {imageUrl && <img src={imageUrl} alt="Uploaded" />}
            </div>
            <div className="button-container">
                <input
                    type="file"
                    ref={fileInputRef}
                    style={{ display: 'none' }}
                    onChange={onFileChange}
                />
                <button className="button_upload n1" onClick={onButtonClick}>
                    Select Reference
                </button>
            </div>
            
            </div>
            {message && <div className="message-popup">{message}</div>}
        </div>
    );
};

export default Matching_upload;
