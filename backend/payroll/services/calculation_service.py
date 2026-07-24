from decimal import Decimal

class SalaryCalculationService:

    @staticmethod 
    def calculate( basic, hra, allowances, pf, tax, other_deductions ):

        basic = Decimal(basic or 0)

        hra = Decimal(hra or 0)

        allowances = Decimal(allowances or 0)

        pf = Decimal(pf or 0)

        tax = Decimal(tax or 0)

        other_deductions = Decimal(
            other_deductions or 0
        )

        gross = ( basic + hra + allowances )

        total_deductions = ( pf + tax + other_deductions )

        net_pay = ( gross - total_deductions )

        return {
            "gross": gross,
            "total_deductions": total_deductions,
            "net_pay": net_pay
        }