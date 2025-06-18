CREATE TABLE image_prediction (
    batch_key UUID,
    product_key UUID,
    image_path TEXT,
    is_mismatch BOOLEAN,
    justification TEXT,
    description_synthesis TEXT,
    image_summary TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY (batch_key, product_key)
); 