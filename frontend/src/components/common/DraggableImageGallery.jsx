import React, { useState } from 'react';
import { DeleteOutlined, DragOutlined } from '@ant-design/icons';
import './DraggableImageGallery.css';

const DraggableImageGallery = ({ images, onImagesChange, maxImages = null }) => {
    const [draggedIndex, setDraggedIndex] = useState(null);
    const [hoveredIndex, setHoveredIndex] = useState(null);

    const handleDragStart = (e, index) => {
        setDraggedIndex(index);
        e.dataTransfer.effectAllowed = 'move';
    };

    const handleDragOver = (e, index) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        setHoveredIndex(index);
    };

    const handleDragLeave = () => {
        setHoveredIndex(null);
    };

    const handleDrop = (e, dropIndex) => {
        e.preventDefault();
        if (draggedIndex === null || draggedIndex === dropIndex) {
            setHoveredIndex(null);
            return;
        }

        const newImages = [...images];
        const draggedImage = newImages[draggedIndex];

        // Remove from old position
        newImages.splice(draggedIndex, 1);
        // Insert at new position
        newImages.splice(dropIndex, 0, draggedImage);

        setDraggedIndex(null);
        setHoveredIndex(null);
        onImagesChange(newImages);
    };

    const handleDragEnd = () => {
        setDraggedIndex(null);
        setHoveredIndex(null);
    };

    const handleRemoveImage = (index) => {
        const newImages = images.filter((_, i) => i !== index);
        onImagesChange(newImages);
    };

    if (!images || images.length === 0) {
        return null;
    }

    return (
        <div className="draggable-gallery">
            {images.map((url, index) => (
                <div
                    key={url}
                    className={`image-item ${draggedIndex === index ? 'dragging' : ''} ${
                        hoveredIndex === index ? 'drag-over' : ''
                    }`}
                    draggable
                    onDragStart={(e) => handleDragStart(e, index)}
                    onDragOver={(e) => handleDragOver(e, index)}
                    onDragLeave={handleDragLeave}
                    onDrop={(e) => handleDrop(e, index)}
                    onDragEnd={handleDragEnd}
                >
                    <img src={url} alt={`Preview ${index + 1}`} className="image-preview" />
                    <div className="image-overlay">
                        <div className="image-actions">
                            <div className="drag-handle" title="Kéo để sắp xếp">
                                <DragOutlined />
                            </div>
                            <button
                                className="delete-btn"
                                onClick={() => handleRemoveImage(index)}
                                title="Xóa ảnh"
                            >
                                <DeleteOutlined />
                            </button>
                        </div>
                        <div className="image-index">{index + 1}</div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default DraggableImageGallery;
