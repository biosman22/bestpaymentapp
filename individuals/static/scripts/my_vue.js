const { createApp } = Vue

var app2 = createApp({
  data() {
    return {
      message: 'Hello Vue!',
      phone_code : "+44",
      id_types:{},
      ewallet_rapyd_id :"",
    }
  } , compilerOptions: {
    delimiters: ["[[", "]]"]
  }
}).mount('#my_app1')
