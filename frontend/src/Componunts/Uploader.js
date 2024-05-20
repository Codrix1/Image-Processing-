import React, { useEffect, useRef, useState } from "react";

const ImageUpload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [message, setMessage] = useState('');
    const [imageUrl, setImageUrl] = useState(null);
    const fileInputRef = useRef(null);

    useEffect(() => {
        fetchImage();
    }, []);

    const fetchImage = () => {
        fetch('http://127.0.0.1:5000/get_Original')
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

        fetch('http://127.0.0.1:5000/upload', {
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

    const onEditClick = () => {
        fetch('http://127.0.0.1:5000/edit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({}) // Send any required data here
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                setMessage('Image edited successfully');
                fetchImage(); // Refresh the image
            } else {
                setMessage(data.error || 'Image edit failed');
            }
        })
        .catch(error => {
            setMessage('Image edit failed');
        });
    };

    const onButtonClick = () => {
        fileInputRef.current.click();
    };

    return (
        <div>
            <div className="image-container">
                {imageUrl && <img src={imageUrl} alt="Uploaded" />}
            </div>
            <div className="button-container">
                <input
                    type="file"
                    ref={fileInputRef}
                    style={{ display: 'none' }}
                    onChange={onFileChange}
                />
                <button className="button_upload" onClick={onButtonClick}>
                    Select File
                </button>
                <button className="button_upload" onClick={onEditClick}>
                    Apply Filter
                </button>
            </div>
            {message && <div className="message-popup">{message}</div>}
        </div>
    );
};

export default ImageUpload;
