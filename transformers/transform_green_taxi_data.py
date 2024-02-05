import inflection

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    print(f"Preprocessing: rows with zero passengers : {data['passenger_count'].isin([0]).sum()}")

    camel_case = [col for col in data.columns if inflection.underscore(col) != col]
    
    
    # camel_case_count = count_camel_case_columns(data)
    print(f"Number of camelCase columns: {len(camel_case)}")

    # data.columns = [inflection.underscore(col) for col in data.columns]

    data.columns = [inflection.underscore(col) for col in data.columns]
    

    # data.columns = (data.columns
    #                 .str.replace(" ", "_")
    #                 .str.lower()
    # )

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    # data['lpep_dropoff_date']= pd.to_datetime(data['lpep_dropoff_datetime'])
    print(f"Vendor ID has these values {data['vendor_id'].unique()}")


    return data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    # return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    existing_vendor_ids = set(output['vendor_id'].unique())

    assert 'vendor_id' in output.columns, 'vendor_id not in the columns'
    assert all(vendor_id in existing_vendor_ids for vendor_id in output['vendor_id']), "Invalid vendor_id found!"
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero trip distance'