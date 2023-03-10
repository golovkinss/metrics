from struct import pack
import os
import pytest
from dbt.tests.util import run_dbt

# our file contents
from tests.functional.fixtures import (
    fact_orders_source_csv,
    fact_orders_sql,
    fact_orders_yml,
)

# models/base_sum_metric.sql
base_sum_metric_sql = """
select *
from 
{{ metrics.calculate(metric('base_sum_metric'), 
    grain='month'
    )
}}
"""

# models/base_sum_metric.yml
base_sum_metric_yml = """
version: 2 
models:
  - name: base_sum_metric
    tests: 
      - metrics.metric_equality:
          compare_model: ref('base_sum_metric__expected')
metrics:
  - name: base_sum_metric
    model: ref('fact_orders')
    label: Total Discount ($)
    timestamp: order_date
    time_grains: [day, week, month]
    calculation_method: sum
    expression: order_total
    dimensions:
      - had_discount
      - order_country
"""

# seeds/base_sum_metric__expected.csv
base_sum_metric__expected_csv = """
date_month,base_sum_metric
2022-01-01,8
2022-02-01,6
""".lstrip()

class TestBaseSumMetric:

    # configuration in dbt_project.yml
    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {
          "name": "example",
          "models": {"+materialized": "table"}
        }

    # install current repo as package
    @pytest.fixture(scope="class")
    def packages(self):
        return {
            "packages": [
                {"local": os.getcwd()}
                ]
        }


    # everything that goes in the "seeds" directory
    @pytest.fixture(scope="class")
    def seeds(self):
        return {
            "fact_orders_source.csv": fact_orders_source_csv,
            "base_sum_metric__expected.csv": base_sum_metric__expected_csv,
        }

    # everything that goes in the "models" directory
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "fact_orders.sql": fact_orders_sql,
            "fact_orders.yml": fact_orders_yml,
            "base_sum_metric.sql": base_sum_metric_sql,
            "base_sum_metric.yml": base_sum_metric_yml
        }

    def test_build_completion(self,project,):
        # running deps to install package
        results = run_dbt(["deps"])

        # seed seeds
        results = run_dbt(["seed"])
        assert len(results) == 2

        # initial run
        results = run_dbt(["run"])
        assert len(results) == 3

        # test tests
        results = run_dbt(["test"]) # expect passing test
        assert len(results) == 1

        # # # validate that the results include pass
        result_statuses = sorted(r.status for r in results)
        assert result_statuses == ["pass"]


# models/base_sum_metric_no_time_grain.sql
base_sum_metric_no_time_grain_sql = """
select *
from 
{{ metrics.calculate(metric('base_sum_metric_no_time_grain'))
}}
"""

# models/base_sum_metric_no_time_grain.yml
base_sum_metric_no_time_grain_yml = """
version: 2 
models:
  - name: base_sum_metric_no_time_grain
    tests: 
      - metrics.metric_equality:
          compare_model: ref('base_sum_metric_no_time_grain__expected')
metrics:
  - name: base_sum_metric_no_time_grain
    model: ref('fact_orders')
    label: Total Discount ($)
    calculation_method: sum
    expression: order_total
    dimensions:
      - had_discount
      - order_country
"""

# seeds/base_sum_metric_no_time_grain__expected.csv
base_sum_metric_no_time_grain__expected_csv = """
base_sum_metric_no_time_grain
14
""".lstrip()

class TestBaseSumMetricNoTimeGrain:

    # configuration in dbt_project.yml
    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {
          "name": "example",
          "models": {"+materialized": "table"}
        }

    # install current repo as package
    @pytest.fixture(scope="class")
    def packages(self):
        return {
            "packages": [
                {"local": os.getcwd()}
                ]
        }


    # everything that goes in the "seeds" directory
    @pytest.fixture(scope="class")
    def seeds(self):
        return {
            "fact_orders_source.csv": fact_orders_source_csv,
            "base_sum_metric_no_time_grain__expected.csv": base_sum_metric_no_time_grain__expected_csv,
        }

    # everything that goes in the "models" directory
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "fact_orders.sql": fact_orders_sql,
            "fact_orders.yml": fact_orders_yml,
            "base_sum_metric_no_time_grain.sql": base_sum_metric_no_time_grain_sql,
            "base_sum_metric_no_time_grain.yml": base_sum_metric_no_time_grain_yml
        }

    def test_build_completion(self,project,):
        # running deps to install package
        results = run_dbt(["deps"])

        # seed seeds
        results = run_dbt(["seed"])
        assert len(results) == 2

        # initial run
        results = run_dbt(["run"])
        assert len(results) == 3

        # test tests
        results = run_dbt(["test"]) # expect passing test
        assert len(results) == 1

        # # # validate that the results include pass
        result_statuses = sorted(r.status for r in results)
        assert result_statuses == ["pass"]