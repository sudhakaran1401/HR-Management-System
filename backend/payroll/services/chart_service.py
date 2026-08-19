from io import BytesIO

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


class PayrollChartService:

    @staticmethod
    def generate_salary_chart(months, totals):

        buffer = BytesIO()

        plt.figure(figsize=(8, 4))

        if len(months) == 1:

            plt.scatter(months, totals)

        else:

            plt.plot( months, totals, marker="o" )

        plt.title("Monthly Net Pay Trend")

        plt.xlabel("Month")

        plt.ylabel("Net Pay")

        plt.tight_layout()

        plt.savefig(
            buffer,
            format="png"
        )

        plt.close()

        buffer.seek(0)

        return buffer