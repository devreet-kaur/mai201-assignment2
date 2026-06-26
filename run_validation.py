import great_expectations as gx

context = gx.get_context()

# rebuild the data source and asset (Ephemeral context does not persist between runs)
datasource = context.data_sources.add_or_update_pandas_filesystem(
    name="customer_data_source",
    base_directory="data/",
)
asset = datasource.add_csv_asset(name="customer_data")

# create a batch definition for the whole CSV
batch_definition = asset.add_batch_definition(name="customer_data_batch")

# rebuild the suite with all eight expectations
suite = gx.ExpectationSuite(name="customer_data_expectations")
suite = context.suites.add_or_update(suite)

suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="customer_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="age", min_value=0, max_value=120))
suite.add_expectation(gx.expectations.ExpectColumnValuesToMatchRegex(
    column="email",
    regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="salary", mostly=0.95))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
    column="country", value_set=["USA", "Canada", "UK", "Australia"],
))
suite.add_expectation(gx.expectations.ExpectColumnValuesToMatchStrftimeFormat(
    column="signup_date", strftime_format="%Y-%m-%d %H:%M:%S",
))
suite.add_expectation(gx.expectations.ExpectTableRowCountToBeBetween(min_value=500, max_value=1000))

# wire the batch definition and suite together
validation_definition = gx.ValidationDefinition(
    name="customer_data_validation",
    data=batch_definition,
    suite=suite,
)
validation_definition = context.validation_definitions.add_or_update(validation_definition)

# wrap it in a checkpoint
checkpoint = gx.Checkpoint(
    name="customer_data_checkpoint",
    validation_definitions=[validation_definition],
)
checkpoint = context.checkpoints.add_or_update(checkpoint)

# run it
results = checkpoint.run()

# print a readable summary
print("\n=== VALIDATION RESULTS ===")
for run_result in results.run_results.values():
    for r in run_result.results:
        status = "PASS" if r.success else "FAIL"
        col = r.expectation_config.kwargs.get("column", "TABLE")
        exp = r.expectation_config.type
        print(f"  [{status}] {col}: {exp}")

# build and open the HTML report
context.build_data_docs()
context.open_data_docs()
print("\nHTML report generated.")