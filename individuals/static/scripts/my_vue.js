const { createApp } = Vue

var app2 = createApp({
  data() {
    return {
      message: 'Hello Vue!',
      phone_code : "+20",
      id_types:{},
    }
  } , compilerOptions: {
    delimiters: ["[[", "]]"]
  }
}).mount('#my_app1')