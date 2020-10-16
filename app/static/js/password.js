function post(endpoint){
    console.log(endpoint)
    var passwordBody = $("#password-container")
      $.post(endpoint, () => {
        console.log(passwordBody)
      })
  }