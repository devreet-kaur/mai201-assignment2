import great_expectations as gx

# connect to the project
context = gx.get_context()

# add a pandas filesystem data source pointing at the data folder
datasource = context.data_sources.add_or_update_pandas_filesystem(
    name="customer_data_source",
    base_directory="data/",
)

# add the asset (the CSV file)
asset = datasource.add_csv_asset(name="customer_data")

# create a batch request
batch_request = asset.build_batch_request()

# create the expectation suite
suite = gx.ExpectationSuite(name="customer_data_expectations")
suite = context.suites.add_or_update(suite)

# open a validator
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="customer_data_expectations",
)

# Expectation 1: customer_id must be unique
validator.expect_column_values_to_be_unique("customer_id")

# Expectation 2: customer_id must not be null
validator.expect_column_values_to_not_be_null("customer_id")

# Expectation 3: age between 0 and 120
validator.expect_column_values_to_be_between("age", min_value=0, max_value=120)

# Expectation 4: email must match a valid format
validator.expect_column_values_to_match_regex(
    "email",
    regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
)

# Expectation 5: salary present in at least 95% of rows
validator.expect_column_values_to_not_be_null("salary", mostly=0.95)

# Expectation 6: country must be one of the allowed values
validator.expect_column_values_to_be_in_set(
    "country", value_set=["USA", "Canada", "UK", "Australia"]
)

# Expectation 7: signup_date must match a parseable datetime format
validator.expect_column_values_to_match_strftime_format(
    "signup_date", strftime_format="%Y-%m-%d %H:%M:%S"
)

# Expectation 8: row count between 500 and 1000
validator.expect_table_row_count_to_be_between(min_value=500, max_value=1000)

# save the suite
context.suites.add_or_update(validator.expectation_suite)
print("Expectation suite saved.")