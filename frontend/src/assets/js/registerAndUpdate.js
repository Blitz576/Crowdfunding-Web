  class FunctionsClass {
    constructor() {
  
    }
    async created(par) {
        try {
            const response = await fetch('https://countriesnow.space/api/v0.1/countries/codes');
            const data = await response.json();
            par.countries=data.data.map((data)=>{
              return data.name
            })
             
        } catch (error) {
            console.error("Error fetching country codes:", error);
        }
    }

    HTMLValidations(e) {
        if (!e.target.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
            e.target.classList.add("was-validated");
            return false;
        } else {
            e.target.classList.add("was-validated");
            return true;
        }
    }

    jsValidations(par,modul)
    {
        const namePattern = /^[a-zA-Z ,.'-]+$/;
        const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
        const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
        const mobilePattern = /^01[012]\d{8}$/;
        const countryPattern = /^[a-zA-Z ,.'-]+$/;
        const birthdatePattern = /^([0-9]{4}[-/]?((0[13-9]|1[012])[-/]?(0[1-9]|[12][0-9]|30)|(0[13578]|1[02])[-/]?31|02[-/]?(0[1-9]|1[0-9]|2[0-8]))|([0-9]{2}(([2468][048]|[02468][48])|[13579][26])|([13579][26]|[02468][048]|0[0-9]|1[0-6])00)[-/]?02[-/]?29)$/;
        const facebookPattern = /^(?:https?:\/\/)?(?:www\.)?(mbasic.facebook|m\.facebook|facebook|fb)\.(com|me)\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)/;
        if(par.country!="")
        {
          if(countryPattern.test(par.country))
              {
                return true;
              }
          else
              {
                return false;
              }
        }
        if(par.birthdate!="")
        {
          if(birthdatePattern.test(par.birthdate))
            {
              return true;
            }
          else
            {
              console.log(par.birthdate)
              return false;
            }
        }
        if(par.facebook!=null)
        {
          if(facebookPattern.test(par.facebook))
              {
                return true;
              }
          else
              {
                console.log(par.facebook)

                return false;
              }
        }
        if (!modul){
          if(passwordPattern.test(par.password))
              {
                return true;
              }
          else
              {
                return false;
              }
        }
        if(
        namePattern.test(par.fname)
        &&namePattern.test(par.lname)
        &&emailPattern.test(par.email)
        &&mobilePattern.test(par.mobile)    
          )
        {
          return true;
        }
        else
        {  
      
          return false;
        }
    }
    projectValidations(par) {
      const titlePattern = /^[a-zA-Z0-9\s]{1,50}$/; // Pattern for alphanumeric and spaces, maximum 50 characters
      const targetPattern = /^\d+$/; // Pattern for positive integers
      const descriptionPattern = /^.{1,400}$/; // Pattern for maximum 255 characters
      
      if (titlePattern.test(par.title)
          && targetPattern.test(par.target)
          && descriptionPattern.test(par.description))
           {
          return true;
      } else {
          console.log(
              titlePattern.test(par.title),
              targetPattern.test(par.target),
              descriptionPattern.test(par.description),
          );
          console.log(
              par.title,
              par.target,
              par.description,
          );
          return false;
      }
  }
  


    confirm(e,par){
         
        if(par.cpassword!=par.password)
        {
          e.target.setCustomValidity("Passwords don't match");
        }
        else
        {
          e.target.setCustomValidity('');
        }
      }

      handleFileChange(event,par)
      {
        par.file = event.target.files[0];
      }
      createForm(par){
        const formData = new FormData();
        formData.append('first_name', par.fname);
        formData.append('last_name',par.lname);
        formData.append('email', par.email);
        formData.append('phone', par.mobile);
        formData.append('birth_date', par.birthdate);
        formData.append('facebook', par.facebook);
         formData.append('country', par.country);
        formData.append('photo', par.file);
        return formData;
      }
      async insertrequest(par)
      {
        const formData=this.createForm(par);
        formData.append('password', par.password);
          try 
          {
            
                const response = await fetch('http://127.0.0.1:8000/api/users/',{
              method: "POST",
              body: formData,
            });
                const data = await response.json(); 
              console.log(data)
          }
        catch (error) 
            {
                console.error("Error fetching api:", error);
            }
      } 
      async updateRequest(par)
      {
        const formData=this.createForm(par);
        if(par.file==null){
          delete formData.photo;
        }
      const localStorageData =JSON.parse(localStorage.getItem('userInfo'));
      const sessionStorageData=JSON.parse(sessionStorage.getItem("userInfo"));
        let token=localStorageData?localStorageData : sessionStorageData 
        token=token.token;
        console.log(token)
          try 
          { 
              const response = await fetch(`http://127.0.0.1:8000/api/users/${par.id}/`,{
              method: "PATCH",
              headers: {
                'Authorization': `token ${token} `
              },
              body: formData,
            });
            
                const data = await response.json(); 
              console.log(data)
          }
        catch (error) 
            {
                console.error("Error fetching api:", error);
            }
      } 

    handleFormSubmission(e,par,modul) {
        if (this.HTMLValidations(e) && this.jsValidations(par,modul)) {
          if(modul){
            
            this.updateRequest(par);
          }else{
            this.insertrequest(par);
          }
           
        }
    }

    async logedInPagesCreated(par){
      const localStorageData =JSON.parse(localStorage.getItem('userInfo'));
      const sessionStorageData=JSON.parse(sessionStorage.getItem("userInfo"));
        if(!sessionStorageData&&!localStorageData){
          par.$router.push('/login');
        }
        else if(localStorageData||sessionStorageData){
          let userData=localStorageData?localStorageData : sessionStorageData 
          par.user=await par.storData.getUserData(userData.user_id,userData.token)
          
        }
      }
}

export default FunctionsClass;


 