CREATE TABLE image_prediction (
    batch_key UUID,
    product_key UUID,
    image_name TEXT,
    attribute_matches_image TEXT,
    description_matches_image TEXT,
    attribute_image_justification TEXT,
    description_image_justification TEXT,
    description_synthesis TEXT,
    image_summary TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY (batch_key, product_key)
); 