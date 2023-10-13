-- SQL script creates index named idx_name_first
-- based first later of the name
CREATE INDEX idx_name_first ON names (name(1));
