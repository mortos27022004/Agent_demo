-- Add table for storing images by attribute combinations
-- This allows uploading images for specific attribute combinations like "Red + 14inch"

CREATE TABLE IF NOT EXISTS product_attribute_images (
  id                uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id        uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  attribute_combo   jsonb NOT NULL, -- e.g., {"Màu sắc": "Cam", "Kích thước": "14inch"}
  image_urls        text[] NOT NULL, -- Array of image URLs
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_attribute_images_product ON product_attribute_images(product_id);

-- Add comment
COMMENT ON TABLE product_attribute_images IS 'Stores images for specific attribute combinations, e.g., Orange + 14inch';
COMMENT ON COLUMN product_attribute_images.attribute_combo IS 'JSON object mapping attribute names to values';
COMMENT ON COLUMN product_attribute_images.image_urls IS 'Array of image URLs for this attribute combination';
