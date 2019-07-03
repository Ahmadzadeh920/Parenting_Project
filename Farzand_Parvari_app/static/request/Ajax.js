var key ;

// _______________________________Set csrf Token
$(document).ready(function() {
   var csrfcookie = function() {
    var cookieValue = null,
        name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

//_______________________size file_number:

  function length_file_number(file_number){
      file_number = file_number.toString();
      if (file_number.length<8){
         size_file_number = file_number.length;
         var increase_length = 8- size_file_number;
         for (i=0 ; i<increase_length ; i++){
             file_number = '0'+ file_number;
         }
         return file_number;
      }
      else{
          return file_number;
      }
  }

//________________ Active Request Fields________
    function Covert_int_to_string_active_request(int_active){
      if(int_active==1){
          str_active_request= 'در حال انتظار ';
      }
      else if(int_active==2){
          str_active_request= 'مورد تایید قرار گرفته است ';
      }
      else {
        str_active_request= 'از طرف مشاور این درخواست رد شده است ';
      }
      return str_active_request
    }

//______________________________Date activate-

    function Date_active_request(date){
      if(date==null){
          str_date= 'هنوز درخواست تایید نشده است ';
      }
      else {
         str_date= date;
      }
      return str_date
    }





//_____________________________Login Form

 $("#loginform").submit(function (e) {
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'html',
                 url: "../../rest_login/",
                data:JSON.stringify({
                    "username": $('#username').val(),
                    "password": $('#password').val(),

                }),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        key_json= $.parseJSON(msg);
                        key=key_json['key'];
                        Cookies.set('token', key);
                        $(window.location).attr('href','../../');
                        //console.log(key)
                         },
                error: function (errormessage) {
                        if (errormessage.responseText){
                                                    $('#result_login').css('color','red')
                                                    $('#result_login').html('نام کاربری و رمز عبور نا درست می باشد');
                                                    }

                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                    }

            }) // end of ajax
        return false;
            }) //end of submit


//----------------------------------------------log out
    $("#logout").click(function (e) {
        $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'html',
                 url: $(this).attr('data-href-template'),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        document.location.href="/";
                         },

                 headers: {
                        'X-CSRFToken': csrfcookie(),
                    }

            }) // end of ajax

    })  // end of click logout

//----------------------------------------------- change password
$("#change_password_form").submit(function (e) {
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'html',
                 url: "../../rest_password_change/",
                data:JSON.stringify({
                    "old_password": $('#old_password').val(),
                    "new_password1": $('#new_password1').val(),
                    "new_password2": $('#new_password2').val(),

                }),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $(window.location).attr('href','../login/');
                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function (errormessage) {
                     $('#result_changePassword').css('color','red')
                    $('#result_changePassword').html(' <br/>رمز عبور صحیح نمی باشد .'+'رمز عبور ها یکسان نمی باشند');
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                    }

            }) // end of ajax
        return false;
            }) //end of submit

//________________________________________________Reset password

$("#form_create_profile_parents").submit(function (e) {
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'html',
                 url: "../Profile_Parents_Create/",

                data:JSON.stringify(
                    {
                         "Birth_date":$('#Birth_date_parent_form').val(),
                         "matrial_status":$('#matrial_status_parent_form').val(),
                          "jobs":$('#jobs_parent_form').val(),
                          "education_degree":$('#education_degree_parent_form').val()
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {

                        $('#jobs_Parents').html(msg.jobs);
                        $('#matrial_status').html(msg.matrial_status);
                        $('#birth_data_Parents').html(msg.Birth_date);
                        $('#graduate_Parents').html(msg.education_degree);
                        $('#result_create_profile_parents').css('color','green');
                        $('#result_create_profile_parents').html('با تشکر از تکمیل پروفایل');

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                             $('#result_create_profile_parents').css('color','red')
                            $('#result_create_profile_parents').html(' <br/>تاریخ تولد خود را وارد نمایید');
                             console.log(jq)
                             }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit

//___________________________________________________Update Profile parents


    $("#form_update_profile_parents").submit(function (e) {
        // if date_birthday is empty
        if ($('#Birth_date_parent_form').val() ==''){
            var Birth_date=$('#birth_data_Parents').html();
            var day = new Date(Birth_date).getDay();
            var month = new Date(Birth_date).getMonth() + 1;
            var year= new Date(Birth_date).getFullYear();
            if (day < 10) {
                day = "0" + day;
                }
            if (month < 10) {
                month = "0" + month;
                }
        var data_birth_date = year+ "-" + month + "-" + day;

        }
        else {
           var data_birth_date=$('#Birth_date_parent_form').val();
        }
            $.ajax({
                type:"PUT",
                "method": "PUT",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../Profile_Parents_Update/",

                data:JSON.stringify(
                    {
                         "Birth_date":data_birth_date,
                         "matrial_status":$('#matrial_status_parent_form').val(),
                          "jobs":$('#jobs_parent_form').val(),
                          "education_degree":$('#education_degree_parent_form').val()
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {

                        $('#jobs_Parents').html(msg.jobs);
                        $('#matrial_status').html(msg.matrial_status);
                        $('#birth_data_Parents').html(msg.Birth_date);
                        $('#graduate_Parents').html(msg.education_degree);
                        $('#result_create_profile_parents').css('color','green')
                        $('#result_create_profile_parents').html('بروزرسانی با موفقیت انجام شد')

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_create_profile_parents').css('color','red'),
                        $('#result_create_profile_parents').html('تاریخ تولد را مجدد وارد نمایید')
                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit

// ---------------------------------------------------- Create profile psychology
     $("#form_create_profile_psy").submit(function (e) {
        // if date_birthday is empty

            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../Profile_Psychology_Create/",

                data:JSON.stringify(
                    {
                        "during_session":$('#during_session_psy_form').val(),
                         "Code_organization":$('#Code_organization_psy_form').val(),
                         "education_degree":$('#education_degree_psy_form').val(),
                         "price":$('#price_psy_form').val(),
                        "Specialist_in_Field_work" :$('#Specialist_in_Field_work_psy_form').val(),
                        "biography":$('#biography_psy_form').val(),
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#during_session_psy').html(msg.during_session);
                        $('#Code_organization_psy').html(msg.Code_organization);
                        $('#education_degree_psy').html(msg.education_degree);
                        $('#price_psy').html(msg.price);
                        $('#Specialist_in_Field_work_psy').html(msg.Specialist_in_Field_work);
                        $('#biography_psy').html(msg.biography);
                        $('#result_create_profile_parents').css('color','green');
                        $('#result_create_profile_parents').html(' با موفقیت انجام شد');

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_create_profile_parents').css('color','red'),
                        $('#result_create_profile_parents').html('تمامی فیلدها الزامی است')

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit


//________________________________Update profile psy

    $("#form_update_profile_psy").submit(function (e) {
        // if date_birthday is empty

            $.ajax({
                type:"PUT",
                "method": "PUT",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../Profile_Psychology_Update/",

                data:JSON.stringify(
                    {
                        "during_session":$('#during_session_psy_form').val(),
                         "Code_organization":$('#Code_organization_psy_form').val(),
                         "education_degree":$('#education_degree_psy_form').val(),
                         "price":$('#price_psy_form').val(),
                        "Specialist_in_Field_work" :$('#Specialist_in_Field_work_psy_form').val(),
                        "biography":$('#biography_psy_form').val(),
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#during_session_psy').html(msg.during_session);
                        $('#Code_organization_psy').html(msg.Code_organization);
                        $('#education_degree_psy').html(msg.education_degree);
                        $('#price_psy').html(msg.price);
                        $('#Specialist_in_Field_work_psy').html(msg.Specialist_in_Field_work);
                        $('#biography_psy').html(msg.biography);
                        $('#result_create_profile_parents').css('color','green');
                        $('#result_create_profile_parents').html('بروز رسانی با موفقیت انجام شد');

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_create_profile_parents').css('color','red'),
                        $('#result_create_profile_parents').html('تمامی فیلدها الزامی است')
                        console.log(jq)

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit

// -------------------------  Children
$("#form_create_child").submit(function (e) {
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                 url: "../Children_Create/",

                data:JSON.stringify(
                    {
                        "name" : $('#name_child_form').val(),
                        "family" : $('#family_child_form').val(),
                         "date_birthday":$('#Birth_date_child_form').val(),
                         "grade_Educations":$('#education_degree_child_form').val(),
                         "disability":$('#disability_child_form').val(),
                        "mental_problems": $('#mental_problems_child_form').val(),
                        "Physical_problems": $('#Physical_problems_child_form').val(),

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                         var html_now= $('#list_children_tbody').html()+"<tr>";
                         var file_number = "<td>"+msg.file_number+"</td>"
                         var name =  "<td>"+msg.name+"</td>";
                         var link_update = "<td> <a href="+msg.file_number+">بروزرسانی پروفایل فرزند</a></td>" ;
                         var select ="<td> <a href=../render_file_number/"+msg.file_number+">انتخاب پرونده</a></td>" ;
                         $('#list_children_tbody').html(html_now+file_number+name+link_update+select+"</tr>");
                        $('#result_create_profile_parents').css('color','green');
                        $('#result_create_profile_parents').html('پروند فرزند تشکیل شد');
                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                             $('#result_create_profile_parents').css('color','red')
                            $('#result_create_profile_parents').html(' <br/>تاریخ تولد خود را وارد نمایید');
                             console.log(jq)
                             }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit
//_______________________________ update profile chidrens
    $("#form_update_child").submit(function (e) {
        // if date_birthday is empty
        if ($('#Birth_date_child_form_update').val() ==''){
            var Birth_date=$('#date_birthday_child_update').html();
            var day = new Date(Birth_date).getDay();
            var month = new Date(Birth_date).getMonth() + 1;
            var year= new Date(Birth_date).getFullYear();
            if (day < 10) {
                day = "0" + day;
                }
            if (month < 10) {
                month = "0" + month;
                }
        var data_birth_date = year+ "-" + month + "-" + day;

        }
        else {
           var data_birth_date=$('#Birth_date_child_form_update').val();
        }
        var file_number = length_file_number($('#hidden_file_number').val())
            $.ajax({
                type:"PUT",
                "method": "PUT",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../Children_Retrive_Update/"+ file_number +"/",

                data:JSON.stringify(
                    {   "name" : $('#hidden_name_child').val(),
                        "family" : $('#hidden_family_child').val(),
                         "date_birthday":data_birth_date,
                         "grade_Educations":$('#education_degree_child_form_update').val(),
                         "disability":$('#disability_child_form_update').val(),
                        "mental_problems": $('#mental_problems_child_form_update').val(),
                        "Physical_problems": $('#Physical_problems_child_form_update').val(),

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#date_birthday_child_update').html(msg.date_birthday);
                        $('#grade_Educations').html(msg.grade_Educations);
                        $('#mental_problems').html(msg.mental_problems);
                        $('#Physical_problems').html(msg.Physical_problems);
                        $('#result_create_profile_parents').css('color','green')
                        $('#result_create_profile_parents').html('بروزرسانی با موفقیت انجام شد')

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_create_profile_parents').css('color','red'),
                        $('#result_create_profile_parents').html('مجدد سعی شود')
                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit

//_______________________________ Training
       var training_steps_json = '';

    $("#training_tab").click(function (e) {
        var file_number_id= $('#hidden_file_number_html').val();

            $.ajax({
                type:"GET",
                "method": "GET",
                dataType: 'json',
                 url: "../../Steps_Training_List/",
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        training_steps_json = msg.results;
                        $('#id_Steps_training').val(training_steps_json[0].id)
                        $('#name_Steps').html(training_steps_json[0].name_Steps);
                        $('#text_Training_steps').html(training_steps_json[0].text_Training_steps);
                        $('#example_Training_steps').html(training_steps_json[0].example_Training_steps);
                        $('#question_common_Training_steps').html(training_steps_json[0].question_common_Training_steps);
                        var url_comments = '../../render_Comments_training/'+file_number_id+'/'+training_steps_json[0].id+'/';
                        $('#Link_comments_Training_steps').attr("href" , url_comments);

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                             console.log(jq)
                             }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax

            }) //end of click training

//-----------------------------------------------------steps of training
    $("#list_step_training li").click(function (e) {
        index=$(this).index();
        var file_number_id= $('#hidden_file_number_html').val();
        if (training_steps_json.length>index) {
            $('#id_Steps_training').val(training_steps_json[index].id)
            $('#name_Steps').html(training_steps_json[index].name_Steps);
            $('#text_Training_steps').html(training_steps_json[index].text_Training_steps);
            $('#example_Training_steps').html(training_steps_json[index].example_Training_steps);
            $('#question_common_Training_steps').html(training_steps_json[index].question_common_Training_steps);
            var url_comments = '../../render_Comments_training/'+file_number_id+'/'+training_steps_json[index].id+'/';
            $('#Link_comments_Training_steps').attr("href" , url_comments);

            $('#list_exercise').html('')
        }
        else {
            $('#id_Steps_training').val('')
           $('#name_Steps').html('');
            $('#text_Training_steps').html('');
            $('#example_Training_steps').html('');
            $('#question_common_Training_steps').html('');
            $('#list_exercise').html('')
            $('#Link_comments_Training_steps').attr("href" , '#');

        }

            }) //end of click training

//__________________________________________
    var Exrecise_training = '';
    var click_exercise = true ;
    $('#Link_Excercise_Training_steps').click(function (e) {
        training_id= $('#id_Steps_training').val();
        var file_number_id= $('#hidden_file_number_html').val()
        if (training_id && click_exercise) {
            $.ajax({
                type: "GET",
                "method": "GET",
                dataType: 'json',
                url: "../../Steps_Exercise_List/"+training_id+"/",
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                    Exrecise_training = msg.results;
                    $('#list_exercise').html('');

                    for (i=0 ; i<Exrecise_training.length; i++){
                        var befor_html_li_exer = $('#list_exercise').html();
                        var merge_html='<li><i class="fa  fa-list-alt"><strong>'+Exrecise_training[i].exercise_name+'</strong></i><p>'+Exrecise_training[i].exercise_text+'</p>';
                        var url_render_answer_exe = '../../render_answer_Exe/'+file_number_id+'/'+Exrecise_training[i].id+'/';
                        var merge_link_slove = '<a class="fa-paper-plane" href="'+url_render_answer_exe+'"> حل تمرین کلیک کنید</a>';

                        $('#list_exercise').html(befor_html_li_exer +merge_html+merge_link_slove);
                        click_exercise = false;

                    }// end of for;



                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader('Authorization', 'Token ' + Cookies.get('token'));
                },
                error: function (jq, status, message) {
                    if (status) {
                        console.log(jq)
                    }
                },
                headers: {
                    'X-CSRFToken': csrfcookie(),
                    'Authorization': 'Token ' + Cookies.get('token')
                }

            }) // end of ajax
        } //end of if
        else {
                $('#list_exercise').html('');
                click_exercise = true;

        }//end of else




}) //end of click Exercise

//__________________________________________________Answer Execise

$("#form_create_answer").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_answer_html').val());
        var exercise_id = $('#hidden_id_exercise_answer_html').val();

            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_Answer_exer/"+file_number+'/'+exercise_id+'/',

                data:JSON.stringify(
                    {
                        "Answer":$('#textarea_answer_exer').val(),

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#Answer').html(msg.Answer);
                        $('#hidden_answer_id_answer_html').val(msg.id)
                        $('#result_answer_exer').css('color','green');
                        $('#result_answer_exer').html(' حل تمرین شما با موفقیت انجام شد');

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_answer_exer').css('color','red'),
                        $('#result_answer_exer').html('فیلد پاسخ نمی تواند خالی باشد')

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create Answer)

//______________________________________________-
$("#form_update_answer").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_answer_html').val());
        var exercise_id = $('#hidden_id_exercise_answer_html').val();

            $.ajax({
                type:"PUT",
                "method": "PUT",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Update_Answer_exer/"+file_number+'/'+exercise_id+'/',

                data:JSON.stringify(
                    {
                        "Answer":$('#textarea_answer_exer').val(),

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#comments').html(msg.Comments);
                        $('#result_comments_training').css('color','green');
                        $('#result_comments_training').html(' بروزرسانی حل تمرین شما با موفقیت انجام شد');

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_comments_training').css('color','red'),
                        $('#result_comments_training').html('فیلد پاسخ نمی تواند خالی باشد')

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit

//_____________________________



//______________________________________________-
$("#form_create_comments_training").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_comments_training_html').val());
        var step_id = $('#hidden_id_step_in_comments_training_html').val();

            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_Comments_Steps/"+file_number+'/'+step_id+'/',

                data:JSON.stringify(
                    {
                        "Comments":$('#textarea_comments_training').val(),

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#comments').html(msg.Comments);
                        $('#result_comments_training').css('color','green');
                        $('#result_comments_training').html(' ایجاد یاداشت برداری با موفقیت آنجام شد');

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_comments_training').css('color','red'),
                        $('#result_comments_training').html('فیلد یادداشت برداری نمی تواند خالی باشد')

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create Answer)

//__________________________________

    $("#form_update_comments_training").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_comments_training_html').val());
        var step_id = $('#hidden_id_step_in_comments_training_html').val();

            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Update_Comments_Steps/"+file_number+'/'+step_id+'/',

                data:JSON.stringify(
                    {
                        "Comments":$('#textarea_comments_training').val(),

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#comments').html(msg.Comments);
                        $('#result_comments_training').css('color','green');
                        $('#result_comments_training').html(' بروزرسانی یادداشت  شما با موفقیت انجام شد');

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_comments_training').css('color','red'),
                        $('#result_comments_training').html('فیلد یادداشت نمی تواند خالی باشد')

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Update comments)
//________________________________Behaviors ---------------------

    $('#List_behavior_tab').click(function (e) {
        var file_number_id= length_file_number($('#hidden_file_number_html').val());
        $('#list_bahavior_tbody').html('');
            $.ajax({
                type: "GET",
                "method": "GET",
                dataType: 'json',
                url: "../../List_bahavior/" +file_number_id + '/',
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                    if (msg.results.length > 0) {
                        length = msg.results.length;
                        for (i = 0; i < length; i++) {
                            w = i + 1;
                            var html_now = $('#list_bahavior_tbody').html() + "<tr>";
                            var i_th = "<td>" + w + "</td>";
                            var name = "<td>" + msg.results[i].Behavior_name + "</td>";
                            var id= msg.results[i].id;
                             var url = '../../render_behavior/'+file_number_id+'/'+id+'/';
                            var link_select = "<td><a href='"+url+"'>  انتخاب رفتار </a></td>"
                            var end_tr = "</tr>";
                            $('#list_bahavior_tbody').html(html_now + i_th + name + link_select + end_tr);


                        }//end of for

                        w = 0;
                    }//end of if

                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader('Authorization', 'Token ' + Cookies.get('token'));
                },
                error: function (jq, status, message) {
                    if (status) {
                        console.log(jq)
                    }
                },
                headers: {
                    'X-CSRFToken': csrfcookie(),
                    'Authorization': 'Token ' + Cookies.get('token')
                }

            }) // end of ajax



    }) // end of List_behavior_tab click


///________________________________________Form create behavior

    $("#form_create_behaviors").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../Create_bahavior/"+file_number+'/',

                data:JSON.stringify(
                    {
                        "Behavior_name":$('#behavior_name_form').val(),

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var html_now = $('#list_bahavior_tbody').html();
                        var w= $('#list_bahavior_tbody tr').length+1 ;
                        var i_th = "<td>"+w+"</td>";
                        var name = "<td>"+msg.Behavior_name+"</td>";
                        var id= msg.id ;
                        var url = '../../render_behavior/'+file_number+'/'+id+'/';
                        var link_select = "<td><a href='"+url+"'>  انتخاب رفتار </a></td>"
                        var end_tr = "</tr>" ;
                        $('#list_bahavior_tbody').html(html_now+i_th+name+link_select+end_tr)
                        $('#result_create_behavior').css('color','green');
                        $('#result_create_behavior').html(' رفتار جدید با موفقیت افزوده شد');
                        w=0;

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_create_behavior').css('color','red'),
                        $('#result_create_behavior').html(' مجدد سعی شود');

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create behavior)
// ____________________________________________________Request


    $('#request_consultant_parent_tab').click(function (e) {
        var file_number_id= $('#hidden_file_number_html').val();
        $('#list_request_tbody').html('');

            $.ajax({
                type: "GET",
                "method": "GET",
                dataType: 'json',
                url: "../../List_Request_file_number/" + length_file_number(file_number_id) + '/',
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                    if (msg.results.length > 0) {
                        length = msg.results.length;
                        for (i = 0; i < length; i++) {
                            w = i + 1;
                            var html_now = $('#list_request_tbody').html() + "<tr>";
                            var i_th = "<td>" + w + "</td>";
                            var date_request = "<td>" + msg.results[i].date_request + "</td>";
                            var active_request = "<td>" + Covert_int_to_string_active_request(msg.results[i].activ_req)+ "</td>";
                            var date_active = "<td>" +Date_active_request(msg.results[i].date_active)+ "</td>";
                            var name_psy_request = "<td>" + msg.results[i].first_name_psy+" "+msg.results[i].first_name_psy +"</td>";
                            var link_cost ="../../render_cost_time/"+msg.results[i].id;
                            var td_cost = "<td><a href="+link_cost+">هزینه و زمان    </a></td>";
                            var end_tr = "</tr>";
                            $('#list_request_tbody').html(html_now + i_th + date_request+active_request + date_active +name_psy_request+td_cost+end_tr);


                        }//end of for

                        w = 0;
                    }//end of if

                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader('Authorization', 'Token ' + Cookies.get('token'));
                },
                error: function (jq, status, message) {
                    if (status) {
                        console.log(jq)
                    }
                },
                headers: {
                    'X-CSRFToken': csrfcookie(),
                    'Authorization': 'Token ' + Cookies.get('token')
                }

            }) // end of ajax of request






    }) // end of List request
// ______________________________________Select psy link
    $('.select_psy_link').click(function select_psy_link_func(id_psy){
        var file_number_id= $('#hidden_file_number_html').val();
        var id_psy = $(this).find('input:hidden').val();
        var d = new Date();
        var year = d.getFullYear();
        var month = d.getMonth();
        var day = d.getDay();

        $.ajax({
                type: "POST",
                "method": "POST",
                dataType: 'json',
                url: "../../Create_Request_file_number/" + length_file_number(file_number_id) + '/',
                contentType: "application/json; charset=utf-8", // this
                data:JSON.stringify(
                    {
                        "user_psy":id_psy,

                    }
                ),
                success: function (msg) {
                            w= $('#list_request_tbody tr').length+1
                            var html_now = $('#list_request_tbody').html() + "<tr>";
                            var i_th = "<td>" + w + "</td>";
                            var date_request = "<td> "+year+"-"+month+"-"+day+"</td>";
                            var active_request = "<td> در حال انتظار</td>";
                            var date_active = "<td>" +Date_active_request(msg.date_active)+ "</td>";
                            var name_psy_request = "<td>" + msg.first_name_psy+" "+msg.last_name_psy +"</td>";
                            var end_tr = "</tr>";
                            $('#list_request_tbody').html(html_now + i_th + date_request+active_request + date_active +name_psy_request+ end_tr);


                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader('Authorization', 'Token ' + Cookies.get('token'));
                },
                error: function (jq, status, message) {
                    if (status) {
                        console.log(jq)
                    }
                },
                headers: {
                    'X-CSRFToken': csrfcookie(),
                    'Authorization': 'Token ' + Cookies.get('token')
                }

            }) // end of ajax of request


})



//---------------------------------------- ####HELper

    $('#add_helper_tab').click(function (e) {
        var file_number_id= $('#hidden_file_number_html').val();
        $('#list_add_helper').html('');

            $.ajax({
                type: "GET",
                "method": "GET",
                dataType: 'json',
                url: "../../List_create_helper_fileNumber/" + length_file_number(file_number_id) + '/',
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                    if (msg.results.length > 0) {
                        length = msg.results.length;
                        for (i = 0; i < length; i++) {
                            w = i + 1;
                            var html_now = $('#list_add_helper').html() + "<tr>";
                            var i_th = "<td>" + w + "</td>";
                            var name = "<td>" + msg.results[i].name +' '+msg.results[i].name  + "</td>";
                            var email = "<td>" + msg.results[i].email+ "</td>";

                            var end_tr = "</tr>";
                            $('#list_add_helper').html(html_now + i_th + name+email+ end_tr);


                        }//end of for

                        w = 0;
                    }//end of if

                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader('Authorization', 'Token ' + Cookies.get('token'));
                },
                error: function (jq, status, message) {
                    if (status) {
                        console.log(jq)
                    }
                },
                headers: {
                    'X-CSRFToken': csrfcookie(),
                    'Authorization': 'Token ' + Cookies.get('token')
                }

            }) // end of ajax of request






    }) // end of List request
// ______________________________________Select helper link
    $('.select_helper_link').click(function select_psy_link_func(id_psy){
        var file_number_id= $('#hidden_file_number_html').val();
        var email_helper = $(this).find('input:hidden').val();

        $.ajax({
                type: "POST",
                "method": "POST",
                dataType: 'json',
                url: "../../List_create_helper_fileNumber/" + length_file_number(file_number_id) + '/',
                contentType: "application/json; charset=utf-8", // this
                data:JSON.stringify(
                    {
                        "email":email_helper,

                    }
                ),
                success: function (msg) {
                            if(msg.id){
                               w = $('#list_add_helper tr').length + 1
                                var html_now = $('#list_add_helper').html() + "<tr>";
                                var i_th = "<td>" + w + "</td>";
                                var name = "<td>" + msg.name + ' ' + msg.family + "</td>";
                                var email = "<td>" + msg.email + "</td>";

                                var end_tr = "</tr>";
                                $('#list_add_helper').html(html_now + i_th + name + email + end_tr);
                                $('#result_add_helper_behavior').css('color','green');
                                $('#result_add_helper_behavior').html('همیارمورد نظر به لیست همیارهای شما اضافه شد')
                            }

                            else{
                                $('#result_add_helper_behavior').css('color','green');
                                $('#result_add_helper_behavior').html('همیار انتخاب شده در لیست همیارهای شما می باشد')
                                console.log(msg);
                            }


                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader('Authorization', 'Token ' + Cookies.get('token'));
                },
                error: function (jq, status, message) {
                    $('#result_add_helper_behavior').css('color','red');
                    $('#result_add_helper_behavior').html('مجدد سعی شود ');
                },
                headers: {
                    'X-CSRFToken': csrfcookie(),
                    'Authorization': 'Token ' + Cookies.get('token')
                }

            }) // end of ajax of request


})






///________________________________________Form create descriptions of behaviors

    $("#form_create_description").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
        var behavior_id =$('#hidden_behavior_id_html').val();
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_descript/"+file_number+'/'+behavior_id+'/',

                data:JSON.stringify(
                    {
                        "discrip": $('#descript_descript_behavior_form').val(),
                        "date_time": $('#time_descript_behavior_form').val(),
                        "place": $('#place_descript_behavior_form').val(),
                        "Status_before_bahavior": $('#Status_before_bahavior_descript_behavior_form').val(),
                        "Result_behavior": $('#Result_behavior_descript_behavior_form').val(),
                        "Comments": $('#Comments_descript_behavior_form').val(),
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var html_now = $('#list_descript_bahavior_tbody').html();
                        var user = "<td>"+ +"</td>";
                        var descript =" <td> "+msg.discrip+"</td>";
                        var date_time =" <td> "+msg.date_time+"</td>";
                        var place =" <td> "+msg.place+"</td>";
                        var Status_before_bahavior =" <td> "+msg.Status_before_bahavior+"</td>";
                        var Result_behavior =" <td> "+msg.Result_behavior+"</td>";
                        var Comments =" <td> "+msg.Comments+"</td>";
                        var end_tr = "</tr>" ;
                        $('#list_descript_bahavior_tbody').html(html_now+user+descript+date_time+place+Status_before_bahavior+Result_behavior+Comments+end_tr)
                        $('#result_create_descript').css('color','green');
                        $('#result_create_descript').html('توصیف از رفتار با موفقیت افزوده شد');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_create_descript').css('color','red'),
                        $('#result_create_descript').html(' مجدد سعی شود . پر کردن تمامی فیلد ها الزامی است');

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create behavior)

//_______________________________________________Update descriptions
    $("#form_update_descript_behavior").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_update_descript_html').val());
        var behavior_id =$('#hidden_behavior_id_update_descript_html').val();
        var descript_id =$('#hidden_descript_id_update_descript_html').val();
        var discrip_text =  $('#descript_descript_behavior_form').val();
            if (discrip_text==''){discrip_text = $('#descript_update_descript').html() ;}
        var date_time_descript =$('#time_descript_behavior_update_form').val();
            if (date_time_descript==''){
                    date_time_before=$('#date_time_update_descript').html();

                    var day = new Date(date_time_before).getDay();
                    var month = new Date(date_time_before).getMonth() + 1;
                    var year= new Date(date_time_before).getFullYear();
                    if (day < 10) {
                    day = "0" + day;
                        }
                    if (month < 10) {
                        month = "0" + month;
                        }
                var date_time_descript = year+ "-" + month + "-" + day;
                        }

        var place_descript =$('#place_descript_behavior_update_form').val();
            if (place_descript==''){place_descript=$('#place_update_descript').html() ;}
        var Status_before_bahavior =$('#Status_before_bahavior_descript_behavior_update_form').val();
            if (Status_before_bahavior==''){ Status_before_bahavior=$('#Status_before_bahavior_update_descript').html() ;}
        var Result_behavior =$('#Result_behavior_descript_behavior_update_form').val();
            if (Result_behavior==''){ Result_behavior=$('#Result_behavior_update_descript').html() ;}
        var Comments =$('#Comments_descript_behavior_update_form').val();
            if (Comments==''){ Comments=$('#Comments_update_descript').html() ;}

            $.ajax({
                type:"PUT",
                "method": "PUT",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../../Update_descript/"+file_number+'/'+behavior_id+'/'+descript_id+'/',

                data:JSON.stringify(
                    {
                        "discrip": discrip_text,
                        "date_time": date_time_descript,
                        "place":place_descript,
                        "Status_before_bahavior": Status_before_bahavior,
                        "Result_behavior": Result_behavior,
                        "Comments": Comments
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {

                        $('#descript_update_descript').html(msg.discrip)
                        $('#date_time_update_descript').html(msg.date_time)
                        $('#place_update_descript').html(msg.place)
                        $('#Status_before_bahavior_update_descript').html(msg.Status_before_bahavior)
                        $('#Result_behavior_update_descript').html(msg.Result_behavior)
                        $('#Comments_update_descript').html(msg.Comments)

                        $('#result_update_descript').css('color','green');
                        $('#result_update_descript').html('ویرایش توصیف از رفتار با موفقیت انجام شد');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        console.log(jq)
                        $('#result_update_descript').css('color','red'),
                        $('#result_update_descrip').html(' مجدد سعی شود');

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit Update rows of discriptions

//_______________________________________Weekly_descripti_behaviors

    $("#form_create_weekly_description").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
        var behavior_id =$('#hidden_behavior_id_html').val();
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_record_weekly/"+file_number+'/'+behavior_id+'/',

                data:JSON.stringify(
                    {
                        "date": $('#time_weekly_descript_behavior_form').val(),
                        "Times": $('#Times_weekly_descript_behavior_form').val(),
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var html_now = $('#list_weekly_descript_bahavior_tbody').html()+"<tr>" ;
                        var user = "<td></td>";
                        var date =" <td> "+msg.date+"</td>";
                        var times =" <td> "+msg.Times+"</td>";
                        var end_tr = "</tr>" ;
                        $('#list_weekly_descript_bahavior_tbody').html(html_now+user+date+times+end_tr)
                        $('#result_create_weekly_descript').css('color','green');
                        $('#result_create_weekly_descript').html(' سطری از جدول هفتگی ایجاد شد ');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_create_weekly_descript').css('color','red'),
                        $('#result_create_weekly_descript').html(' مجدد سعی شود');

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create weekly behaviors)

// ---------------------------------------------------------------- Update
    $("#form_cause_behavior").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
        var behavior_id =$('#hidden_behavior_id_html').val();
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_Cause_file_numbe/"+file_number+'/'+behavior_id+'/',

                data:JSON.stringify(
                    {
                          "Cause": $('input[name=cause]:checked', '#form_cause_behavior').val(),
                        }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var html_now = $('#list_cause_bahavior_tbody').html()+"<tr>" ;
                        var user = "<td></td>";
                        var text_cause = $('input[name=cause]:checked', '#form_cause_behavior').next('label:first').html();
                        var td_txt_cause =" <td> "+text_cause+"</td>";
                        var descript_cause = $('input[name=cause]:checked', '#form_cause_behavior').attr("alt");
                        var td_descript_cause =" <td> "+descript_cause+"</td>";
                        var end_tr = "</tr>" ;
                        $('#list_cause_bahavior_tbody').html(html_now+user+td_txt_cause+td_descript_cause+end_tr)
                        $('#result_cuase_create').css('color','green');
                        $('#result_cuase_create').html(' سطری از جدول هفتگی ایجاد شد ');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_cuase_create').css('color','red'),
                        $('#result_cuase_create').html(' مجدد سعی شود');

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create Cause)

    //__________________________________________

    $("#form_create_reward").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
        var behavior_id =$('#hidden_behavior_id_html').val();
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_Reward_behavior/"+file_number+'/'+behavior_id+'/',

                data:JSON.stringify(
                    {
                             "Reward_txt": $('#Reward_txt_behavior_form').val(),
                            "Reward_descript": $('#Reward_descript_behavior_form').val() ,
                            "type_of_Reward" : $('input[name=type_reward]:checked', '#form_create_reward').val(),
                        }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var html_now = $('#list_reward_bahavior_tbody').html()+"<tr>" ;
                        var text_reward = msg.Reward_txt;
                        var td_text_reward =" <td> "+text_reward+"</td>";
                        var descript = msg.Reward_descript;
                        if (descript){var td_descript =" <td> "+descript+"</td>";}
                        else{var td_descript =" <td> "+''+"</td>";}
                        var type_td = " <td> "+$('input[name=type_reward]:checked', '#form_create_reward').next('label:first').html()+"</td>";
                        var end_tr = "</tr>" ;
                        $('#list_reward_bahavior_tbody').html(html_now+td_text_reward+td_descript+type_td+end_tr)
                        $('#result_reward_create').css('color','green');
                        $('#result_reward_create').html(' پاداش ایجاد شد ');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_reward_create').css('color','red'),
                        $('#result_reward_create').html(' مجدد سعی شود');

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create Rewards)
//-----------------------------------------------------------------
    $("#form_create_rule").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
        var behavior_id =$('#hidden_behavior_id_html').val();
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_Rule_Rewards/"+file_number+'/'+behavior_id+'/',

                data:JSON.stringify(
                    {
                             "Rule_txt": $('#Rule_txt_behavior_form').val(),
                            "Rule_descript": $('#Rule_descript_behavior_form').val() ,

                        }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var html_now = $('#list_rule_bahavior_tbody').html()+"<tr>" ;
                        var text_reward = msg.Rule_txt;
                        var td_text_reward =" <td> "+text_reward+"</td>";
                        var descript = msg.Rule_descript;
                        if (descript){var td_descript =" <td> "+descript+"</td>";}
                        else{var td_descript =" <td> "+''+"</td>";}
                        var end_tr = "</tr>" ;
                        $('#list_rule_bahavior_tbody').html(html_now+td_text_reward+td_descript+end_tr)
                        $('#result_rule_create').css('color','green');
                        $('#result_rule_create').html(' قانون ایجاد شد ');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_rule_create').css('color','red'),
                        $('#result_rule_create').html(' مجدد سعی شود');

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create Rule)


//_______________________________

    $("#form_create_rows_star_table").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
        var behavior_id =$('#hidden_behavior_id_html').val();

            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_Star_Table/"+file_number+'/'+behavior_id+'/',

                data:JSON.stringify(
                    {

                        "reward": $('#select_reward_in_star_table').find(":selected").val(),
                        "rule":$('#select_rule_in_star_table').find(":selected").val(),
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var html_now = $('#list_star_table_tbody').html()+"<tr>" ;
                        var td_text_reward =" <td> "+$('#select_reward_in_star_table').find(":selected").text()+"</td>";
                        var td_text_rule =" <td> "+$('#select_rule_in_star_table').find(":selected").text()+"</td>";
                        var td_star =" <td> "+''+"</td>";
                        var td_link ="<td><a href=\"#\" class=\"add_star_link fa-link\" data-times = \""+msg.times+"\" data-reward-id = \""+msg.reward+"\" data-rule-id=\""+msg.rule+"\"  data-model-name=\""+msg.id+"\">افزودن ستاره</a></td> ";
                        var end_tr = "</tr>" ;
                        $('#list_star_table_tbody').html(html_now+td_text_reward+td_text_rule+td_star+td_link+end_tr)
                        $('#result_rows_star_table_create').css('color','green');
                        $('#result_rows_star_table_create').html(' سطری به جدول ستاره افزوده شد  , به منظور فعال سازی افزودن ستاره لطفا صفحه را refresh ');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_rows_star_table_create').css('color','red'),
                        $('#result_rows_star_table_create').html(' مجدد سعی شود');
                        console.log(jq)

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create rows of star table)
//____________________________________________________________________
    $(".add_star_link").click(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
        var behavior_id =$('#hidden_behavior_id_html').val();
        var id_rows= $(this).attr("data-model-name");
        var id_reward =  $(this).attr("data-reward-id");
        var id_rule =  $(this).attr("data-rule-id");
        var times =  $(this).attr("data-times");
        var html_star = $(this).closest('td').prev('td');
        $.ajax({
                type:"PUT",
                "method": "PUT",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Update_Retrieve_Star_Table/"+file_number+'/'+behavior_id+'/'+id_rows+'/',

                data:JSON.stringify(
                    {

                        "reward": id_reward ,
                        "rule": id_rule ,
                        "times" : parseInt(times)+1,
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var td_i = "<i class=\"fa fa-star-half-full\"></i>";

                       html_star.append(td_i);

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_rows_star_table_create').css('color','red'),
                        $('#result_rows_star_table_create').html(' مجدد سعی شود');
                        console.log(jq)

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax


            }) //end of clicked  (add star of star table)

//__________________________ Punish

    $("#form_create_punish").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
        var behavior_id =$('#hidden_behavior_id_html').val();

            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_punishment_behavior/"+file_number+'/'+behavior_id+'/',

                data:JSON.stringify(
                    {
                        "name":$('#name_punish_behavior_form').val(),
                        "result": $('#result_punish_behavior_form').val(),
                        "descript":$('#descript_punish_behavior_form').val(),
                        "Date_Time":$('#date_punish_behavior_form').val(),
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var html_now = $('#list_punish_bahavior_tbody').html()+"<tr>" ;
                        var td_name =" <td> "+msg.name+"</td>";
                        var td_descript =" <td> "+msg.descript+"</td>";
                        var td_result =" <td> "+msg.results+"</td>";
                        var td_date =" <td> "+msg.Date_Time+"</td>";

                        var end_tr = "</tr>" ;
                        $('#list_punish_bahavior_tbody').html(html_now+td_name+td_descript+td_result+td_date+end_tr)
                        $('#result_punish_create').css('color','green');
                        $('#result_punish_create').html(' سطری به جدول وضعیت دشوار افزوده شد ');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_punish_create').css('color','red'),
                        $('#result_punish_create').html(' مجدد سعی شود');


                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create rows of Punish table)

//________________________________________________________
    $("#form_create_difficult_situation").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
        var behavior_id =$('#hidden_behavior_id_html').val();
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_Situation_behavior/"+file_number+'/'+behavior_id+'/',

                data:JSON.stringify(
                    {
                        "name": $('#name_difficult_situation_form').val(),
                        "grade":$('#select_grade_difficult_situation').find(":selected").val(),
                        "Date_Time": $('#date_difficult_situation_behavior_form').val(),
                        "comments": $('#comments_difficult_situation_behavior_form').val(),
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var html_now = $('#list_difficult_bahavior_tbody').html()+"<tr>" ;
                        var td_name =" <td> "+msg.name+"</td>";
                        var td_descript =" <td> "+msg.comments+"</td>";
                        var td_date =" <td> "+msg.Date_Time+"</td>";
                        var td_grade =" <td> "+msg.grade+"</td>";
                        var end_tr = "</tr>" ;
                        $('#list_difficult_bahavior_tbody').html(html_now+td_name+td_descript+td_date+td_grade+end_tr)
                        $('#result_difficult_create').css('color','green');
                        $('#result_difficult_create').html(' سطری به جدول جریمه افزوده شد ');
                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_difficult_create').css('color','red'),
                        $('#result_difficult_create').html(' مجدد سعی شود');


                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create rows of Punish table)
//__________________________________________________________________Form create surprise

    $("#form_create_suprise").submit(function (e) {
        var file_number =length_file_number($('#hidden_file_number_html').val());
        var behavior_id =$('#hidden_behavior_id_html').val();
        var max= $('#suprise_hidden_form').val()-1; //
        var min=0;
        var random_number = Math.floor(Math.random()*(max-min+1)+min);
        var id_reward = $('#list_reward_bahavior_tbody tr').get(random_number).getElementsByTagName('input').item(0).value;
        var text_reward =  $('#list_reward_bahavior_tbody tr').get(random_number).getElementsByTagName('td').item(0).innerText;

        var d = new Date();
        var date = d.getFullYear() + "/" + (d.getMonth()+1) + "/" + d.getDate();
        $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../../Create_Surprise_Table/"+file_number+'/'+behavior_id+'/',
                data:JSON.stringify(
                    {
                        "Reward":id_reward
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        var html_now = $('#list_suprise_tbody').html()+"<tr>" ;
                        var td_reward =" <td> "+text_reward+"</td>";
                        var td_date =" <td>"+date+"</td>";
                        var end_tr = "</tr>" ;
                        $('#list_suprise_tbody').html(html_now+td_reward+td_date+end_tr);
                        $('#result_suprise_create').css('color','green');
                        $('#result_suprise_create').html(text_reward+ 'جایزه ی امروز شما ' );
                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_suprise_create').css('color','red'),
                        $('#result_suprise_create').html(' مجدد سعی شود');

                        console.log(jq)
                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax

        return false;
            }) //end of submit (Create rows of surprise table)
// ------------------------------------------- Psychology Cost_time
    $("#form_create_cost_time_request").submit(function (e) {
        var id_request =$('#hidden_id_request').val();

            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../Create_time_cost_request/"+id_request+'/',

                data:JSON.stringify(
                    {
                         "duration":$('#duration_cost_time_form').val(),
                        "Cost": $('#cost_time_form').val(),
                        "comment": $('#comments_time_form').val(),

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#duration').html(msg.duration);
                        $('#cost').html(msg.Cost);
                        $('#comments_cost').html(msg.comment);
                         $('#result_create_cost_time').css('color','green');
                        $('#result_create_cost_time').html('هزینه و تعداد ساعاتی که برای پرونده درج شد');
                        console.log(msg);

                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_create_cost_time').css('color','red'),
                        $('#result_create_cost_time').html('مجدد سعی شود تمامی فیلدها الزامی است')

                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create Cost_time)

//______________________________________________Update cost and time
    $("#form_update_cost_time_request").submit(function (e) {
        var id_request =$('#hidden_id_request').val();

            $.ajax({
                type:"PUT",
                "method": "PUT",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../Update_Retrieve_time_cost_request/"+id_request+'/',

                data:JSON.stringify(
                    {
                         "duration":$('#duration_cost_time_form').val(),
                        "Cost": $('#cost_time_form').val(),
                        "comment": $('#comments_time_form').val(),

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#duration').html(msg.duration);
                        $('#cost').html(msg.Cost);
                        $('#comments_cost').html(msg.comment);
                         $('#result_create_cost_time').css('color','green');
                        $('#result_create_cost_time').html('هزینه و تعداد ساعاتی که برای پرونده ویرایش شد');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_create_cost_time').css('color','red');
                        $('#result_create_cost_time').html('مجدد سعی شود تمامی فیلدها الزامی است');



                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Update Cost_time)

//////_________________ Active Request

    $(".activate_request_link").click(function (e) {
        var id_request =$(this).attr('data-id-request');
        var td = $(this).parent();

            $.ajax({
                type:"PUT",
                "method": "PUT",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../Change_status_request/"+id_request+'/',

                data:JSON.stringify(
                    {
                         "activ_req":2,

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        td.html('');
                        td.css('color','green');
                         td.html('فعال سازی پرونده انجام شد');
                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        td.css('color','red');
                         td.html('مجدد سعی شود');
                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Update Cost_time)
//___________________________________________________________Create general noting

    $("#form_create_total_noting").submit(function (e) {

            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../List_create_general_nothing/",

                data:JSON.stringify(
                    {
                         "txt": $('#txt_total_noting_form').val()

                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#list_total_noting_tbody').append("<tr><td>"+msg.txt+"</td></tr>")
                         $('#result_total_noting_create').css('color','green');
                        $('#result_total_noting_create').html('یادداشت جدید ثبت شد');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_total_noting_create').css('color','red');
                        $('#result_total_noting_create').html('مجدد سعی شود تمامی فیلدها الزامی است');



                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create general noting)

//-------------------------- Create Agenda
    $("#form_create_agenda").submit(function (e) {
    var file_number =$('#hidden_id_file_number').val();
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../Create_Agenda/"+length_file_number(file_number)+'/',

                data:JSON.stringify(
                    {
                        "name": $('#name_agenda_form').val(),
                        "descript": $('#descript_agenda_form').val(),
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#list_agenda_file_number_tbody').append("<tr><td>"+msg.name+"</td> <td>"+msg.descript+"</td><td></td></tr>")
                         $('#result_create_agenda_file_number').css('color','green');
                        $('#result_create_agenda_file_number').html('دستور کار  جدید ثبت شد');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_create_agenda_file_number').css('color','red');
                        $('#result_create_agenda_file_number').html('مجدد سعی شود تمامی فیلدها الزامی است');



                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create general noting)
    //---------------------------------------
    $("#form_create_noting_file_number").submit(function (e) {
    var file_number =$('#hidden_id_file_number_noting_file_number').val();
            $.ajax({
                type:"POST",
                "method": "POST",
                dataType: 'json',
                enctype: 'multipart/form-data',
                processData: false,  // Importa
                 url: "../../List_create_noting_fileNumber/"+length_file_number(file_number)+'/',

                data:JSON.stringify(
                    {
                        "txt":$('#txt_noting_file_number_form').val()
                    }
                ),
                contentType: "application/json; charset=utf-8", // this
                success: function (msg) {
                        $('#list_noting_file_number_tbody').append("<tr><td>"+msg.txt+"</td></tr>")
                         $('#result_noting_file_number').css('color','green');
                        $('#result_noting_file_number').html('یادداشت  جدید ثبت شد');


                         },
                beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','Token '+Cookies.get('token')); },
                error: function(jq,status,message) {
                    if (status){
                        $('#result_noting_file_number').css('color','red');
                        $('#result_noting_file_number').html('مجدد سعی شود تمامی فیلدها الزامی است');



                        }
                    },
                 headers: {
                        'X-CSRFToken': csrfcookie(),
                        'Authorization': 'Token '+Cookies.get('token')
                    }

            }) // end of ajax
        return false;
            }) //end of submit (Create noting for file number)
//---------------------------------------------------



 })// end of document ready

