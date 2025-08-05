# Sample SKU data
sku_data = {
    'pen': 'cste-pen',
    'pen-blue': 'cste-pen',
    'pen-blue2': 'cste-pen-black',
    'cste-pen': 'cste-pen',  # Ensure all components are mapped
    'cste-pen-black': 'cste-pen-black'
}

class SKUMapper:
    def __init__(self, sku_data):
        self.sku_data = sku_data
        self.sku_to_msku = {}

    def load_mappings(self):
        # Load SKU to MSKU mappings from data
        for sku, msku in self.sku_data.items():
            self.sku_to_msku[sku] = msku

    def map_sku(self, sku):
        # Map SKU to MSKU
        return self.sku_to_msku.get(sku, None)

    def handle_combo(self, combo_sku):
        components = combo_sku.split('-')
        mapped_components = [self.map_sku(sku) for sku in components]
        if None in mapped_components:
            print("Warning: Some SKUs in the combo are not mapped.")
        return mapped_components



# Initialize SKUMapper
mapper = SKUMapper(sku_data)
mapper.load_mappings()

# Test mapping
print(mapper.map_sku('pen'))  # Should output 'cste-pen'
print(mapper.handle_combo('pen-blue-pen-blue2'))  # Should output ['cste-pen', 'cste-pen-black']