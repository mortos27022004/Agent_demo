import React, { useState, useEffect } from 'react';

const ProductGallery = ({ imageSet, imageIndex, setImageIndex, title }) => {
    const [prevImage, setPrevImage] = useState('');
    const mainImage = imageSet[imageIndex] || '';

    // Track previous image for cross-fade effect
    useEffect(() => {
        if (mainImage) {
            const timer = setTimeout(() => {
                setPrevImage(mainImage);
            }, 400); // Match CSS animation duration
            return () => clearTimeout(timer);
        }
    }, [mainImage]);

    if (!imageSet || imageSet.length === 0) return null;

    return (
        <div className="product-gallery">
            <div className="main-image-wrapper">
                {prevImage && prevImage !== mainImage && (
                    <img
                        src={prevImage}
                        alt=""
                        className="main-image prev-image"
                    />
                )}
                <img
                    key={mainImage}
                    src={mainImage}
                    alt={title}
                    className="main-image"
                />
            </div>
            <div className="thumbnail-list">
                {imageSet.map((url, idx) => (
                    <div
                        key={idx}
                        className={`thumbnail-item ${imageIndex === idx ? 'active' : ''}`}
                        onClick={() => setImageIndex(idx)}
                    >
                        <img src={url} alt={`Thumbnail ${idx}`} />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ProductGallery;
