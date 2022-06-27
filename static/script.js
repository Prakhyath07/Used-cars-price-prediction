console.log("Ajax");
function myFunc() {

  $('#loading').hide();

  $('.res-container').hide();
  $('.disp_image').hide();
}

//let fetchBtn = document.getElementById('button');
//fetchBtn.addEventListener('click', buttonClickHandler)
function submitFormData(event) {
     console.log('You have clicked the fetchBtn');


     // Instantiate an xhr object
     const xhr = new XMLHttpRequest();
     var manufacturer_name = event.manufacturer_name.value;
     var model_name= event.model_name.value;
     var transmission= event.transmission.value;
     var odometer_value= event.odometer_value.value;
     var year_produced= event.year_produced.value;
     var engine_fuel= event.engine_fuel.value;
     var engine_capacity= event.engine_capacity.value;
     var body_type= event.body_type.value;
     var drivetrain= event.drivetrain.value;
     var number_of_photos= event.number_of_photos.value;
     var feature_1= event.feature_1.value;
     var feature_2= event.feature_2.value;
     var feature_3= event.feature_3.value;
     var feature_4= event.feature_4.value;
     var feature_6= event.feature_6.value;
     var feature_7= event.feature_7.value;
     var feature_8= event.feature_8.value;
     var prediction;
     var data = new FormData();
     data.append('manufacturer_name', manufacturer_name);
     data.append('model_name', model_name);
     data.append('transmission', transmission);
     data.append('odometer_value', odometer_value);
     data.append('year_produced', year_produced);
     data.append('engine_fuel', engine_fuel);
     data.append('engine_capacity', engine_capacity);
     data.append('body_type', body_type);
     data.append('drivetrain', drivetrain);
     data.append('number_of_photos', number_of_photos);
     data.append('feature_1', feature_1);
     data.append('feature_2', feature_2);
     data.append('feature_3', feature_3);
     data.append('feature_4', feature_4);
     data.append('feature_6', feature_6);
     data.append('feature_7', feature_7);
     data.append('feature_8', feature_8);
     let date = new Date();
     if ((manufacturer_name=='')||(model_name=='')||(transmission=='')||(odometer_value=='')||(year_produced=='')||(engine_fuel=='')||
     (engine_capacity=='')||(body_type=='')||(drivetrain=='')||(number_of_photos=='')||(feature_1=='')||(feature_2=='')||(feature_3=='')||(feature_4=='')||(feature_6=='')||(feature_7=='')||(feature_8=='')){
        alert("All fields must be filled out");


        return false;

     }


     else if(year_produced>date.getFullYear()){

        alert("Year produced must not be greater than current year");


     }
     else{

            $('#loading').show();
         // Open the object
         xhr.open('POST', '/predict', true);

         // What to do on progress (optional)
         xhr.onprogress = function(){
            console.log('On progress');

            $('#loading').show();


         }

         xhr.onload = function () {
            if(this.status === 200){
                setTimeout(function(){
                    $('#loading').hide();
                },1000);
                prediction = this.responseText;
                console.log(this.responseText)


                $(".result").html('<p>Price of car is:   <strong> '+ this.responseText + ' </strong> Dollars </p>')
                $('.res-container').show();
    //            $('.disp_image').show();
                myFunc2(this.responseText);


            }
            else{
                console.log("Some error occured")
            }


         }

             // send the request
    //     params={manufacturer_name:manufacturer_name,model_name:model_name,transmission:transmission,odometer_value:odometer_value,year_produced:year_produced,engine_fuel:engine_fuel,engine_capacity:engine_capacity,body_type:body_type,drivetrain:drivetrain,number_of_photos:number_of_photos,feature_1:feature_1,feature_2:feature_2,feature_3:feature_3,feature_4:feature_4,feature_6:feature_6,feature_7:feature_7,feature_8:feature_8};
         xhr.send(data);
         console.log("First route complete");

    }



}

function myFunc2(pred) {

  console.log('myfunc2')
  console.log(pred)
  const xhr2 = new XMLHttpRequest();
  // Open the object
     xhr2.open('POST', '/plot.png', false);

     // What to do on progress (optional)
     xhr2.onprogress = function(){
        console.log('On progress');

        $('#loading').show();


     }

     xhr2.onload = function () {
        if(this.status === 200){
//            setTimeout(function(){
//                $('#loading').hide();
//            },1000);
//            prediction = this.responseText;
//            console.log(this.responseText)


//            $(".disp_image").html('<pre>' + this.responseText+'</pre>');
            $("#image").attr('src', this.responseText);
//            $('.res-container').show();
            $('.disp_image').show();



        }
        else{
            console.log("Some error occured")
        }


     }

         // send the request

     data=pred;
     xhr2.send(data);
     console.log("Second route complete");
}

function myFunc3(manufacturer_name) {

  console.log('myfunc3')
  console.log(manufacturer_name)
  const xhr3 = new XMLHttpRequest();
  // Open the object
     xhr3.open('POST', 'model', false);

     // What to do on progress (optional)
     xhr3.onprogress = function(){
        console.log('On progress');

        $('#loading').show();


     }

     xhr3.onload = function () {
        if(this.status === 200){
//            let html_data = '<option value="">---------</option>';
//            data.forEach((this.responseText)  {html_data += '<option value="${data}">${this.responseText[data]}</option>'});
////            $("#image").attr('src', this.responseText);
//            $("#model_name").html(html_data);
//            $('.res-container').show();
            let model_list=$('#model_name');
            var resp=JSON.parse(this.responseText);
            let html_data = '<option value="">---------</option>';
            for([key, val] of Object.entries(resp)) {

              html_data += '<option value='+key+'>'+val+'</option>';

            }
            $("#model_name").html(html_data);


            $('#loading').hide();



        }
        else{
            console.log("Some error occured")
        }


     }

         // send the request

     data=manufacturer_name;
     xhr3.send(data);
     console.log(data);
}