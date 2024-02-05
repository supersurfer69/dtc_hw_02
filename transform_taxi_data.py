if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    taxi_columns_rename = {
        'VendorID': 'vendor_id',
        'RatecodeID': 'rate_code_id',
        'PULocationID': 'pick_up_location_id',
        'DOLocationID': 'drop_off_location_id',
    }
    data = data.rename(columns=taxi_columns_rename)
    print(f"Preprocessing: rows with zero passengers: {data['passenger_count'].isin([0]).sum()}")
    print(f"Preprocessing: rows with zero distance: {data['trip_distance'].isin([0]).sum()}")
    print(f"Existing values of vendor_id is : {data['vendor_id'].unique()}")
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    return data[(data['passenger_count']>0) & (data['trip_distance']>0)]

@test
def test_output(output, *args):
    assert 'vendor_id' in output.columns, 'There are missing column "vendor_id"'
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero distance'
