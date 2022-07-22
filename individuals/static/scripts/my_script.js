$('select#country_list').on('change', function (e) {
  var optionSelected = $("option:selected", this);
  var valueSelected = this.value;
  app2.phone_code = $(optionSelected).attr("phone_code");
  country = $(optionSelected).attr("iso_alpha2");
  $.get(window.location.origin+"/ind/papers?c="+country, function( data ) {
    //$( ".result" ).html( data );
    //alert( "Load was performed."+data );
    var dict = {};
    data.data.forEach(element => {
      dict[element.type] = element.name;
    });

    console.log(data);
    console.log(dict);
    app2.id_types = dict
  });
    
});