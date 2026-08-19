
(function () {

    const amtInput = document.getElementById("id_amt_per_day");
    if (!amtInput) return;

    function calculateSalary() {
        let amt = parseFloat(amtInput.value);

        if (!amt) {
            document.getElementById("id_basic").value = "";
            document.getElementById("id_hra").value = "";
            document.getElementById("id_allowances").value = "";
            document.getElementById("id_pf").value = "";
            document.getElementById("id_tax").value = "";
            document.getElementById("id_other_deductions").value = "";
            return;
        }

        let monthly = amt * 30;

        let basic = monthly * 0.7;
        let hra = monthly * 0.2;
        let allowances = monthly * 0.1;
        let pf = basic * 0.05;
        let tax = basic * 0.02;

        document.getElementById("id_basic").value = basic.toFixed(2);
        document.getElementById("id_hra").value = hra.toFixed(2);
        document.getElementById("id_allowances").value = allowances.toFixed(2);
        document.getElementById("id_pf").value = pf.toFixed(2);
        document.getElementById("id_tax").value = tax.toFixed(2);
        document.getElementById("id_other_deductions").value = 0;
    }

    amtInput.addEventListener("input", calculateSalary);

})();