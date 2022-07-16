$('select').on('change', function (e) {
  var optionSelected = $("option:selected", this);
  var valueSelected = this.value;
  app2.phone_code = $(optionSelected).attr("phone_code")
    
});