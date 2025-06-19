CREATE TABLE image_prediction (
    batch_key UUID,
    product_key UUID,
    image_name TEXT,
    colour_status TEXT,
    colour_justification TEXT,
    description_synthesis TEXT,
    image_summary TEXT,
    final_colour_status TEXT,
    final_colour_justification TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY (batch_key, product_key)
); 