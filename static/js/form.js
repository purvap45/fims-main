$(document).ready(function () {
    // toggle head wedding date 
    $('#wedding_date').hide();
    $('input[name="marital_status"]').on('change', function () {
        if ($(this).val().toLowerCase() === "married") {
            $('#wedding_date').show();
        } else {
            $('#wedding_date').hide();
            $('input[name="wedding_date"]').val('');
        }
    });

    // toggle member wedding date 
    $('#member-container').on('change', 'input[type="radio"][name$="member_marital"]', function () {
        let memberRow = $(this).closest('.member-row');
        memberRow.find('.member-wed').hide();
        if ($(this).is(':checked') && $(this).val().toLowerCase() === "married") {
            memberRow.find('.member-wed').show();
            memberRow.find('input[name$="member_wedDate"]').val('');
        }
    });

    // Add Hobby
    // let formIdx = {{ formset.total_form_count|add:"-1" }};
    let formIdx = $('#id_hobbies-TOTAL_FORMS').val(); 

    $('#addHobby').click(function() {
        let lastInput = $('#hobby-container .hobby-row:last input[type="text"]'); 
        if (lastInput.val().trim() === "") { 
            alert("Please fill the current hobby before adding a new one."); 
            lastInput.focus(); 
            return; 
        }
        $('#hobby-container').append($('#hobby-container .hobby-row:last').clone().find('input').each(function() {
            let name = $(this).attr('name').replace(/-\d+-/, '-' + formIdx + '-');
            let id = $(this).attr('id').replace(/-\d+-/, '-' + formIdx + '-');	
            $(this).attr('name', name);  
            $(this).attr('id', id);
            $(this).val('');
            }).end().find('input[name$=-id]').val('').end().find('.removeHobby').show().end());

        formIdx++;       
        $('#id_hobbies-TOTAL_FORMS').val(formIdx);
    });

    $('#hobby-container').on('click', '.removeHobby', function() {
        $(this).closest('.hobby-row').remove();
        formIdx--; 
        $('#id_form-TOTAL_FORMS').val(formIdx);
    });
    $('.removeHobby').hide();

    let memberIdx = $('#id_members-TOTAL_FORMS').val();

$('#addMember').click(function () {
    // validate last member if exists
    let lastRow = $('#member-container .member-row:last');
    if (lastRow.length) {
        let nameInput = lastRow.find('input[name$="member_name"]');
        if (nameInput.val().trim() === "") {
            alert("Please fill the current member before adding a new one.");
            nameInput.focus();
            return;
        }
    }

    // clone template
    let newRow = $('#member-template .member-row').clone();
    newRow.find('input,label,div').each(function () {
        let name = $(this).attr('name');
        if (name) {
            name = name.replace(/__prefix__/, memberIdx);
            $(this).attr('name', name);
        }
        let id = $(this).attr('id');
        if (id) {
            id = id.replace(/__prefix__/, memberIdx);
            $(this).attr('id', id);
        }
        let labelfor = $(this).attr('for');
        if (labelfor) {
            labelfor = labelfor.replace(/__prefix__/, memberIdx);
            $(this).attr('for', labelfor);
        }
        if ($(this).is(':radio') || $(this).is(':checkbox')) {
            $(this).prop('checked', false);
        } else {
            $(this).val('');
        }
    });

    $('#member-container').append(newRow);
    memberIdx++;
    $('#id_members-TOTAL_FORMS').val(memberIdx);
});

// remove member
$('#member-container').on('click', '.removeMember', function () {
    $(this).closest('.member-row').remove();
    // do NOT decrement TOTAL_FORMS (Django expects count of forms rendered)
});


    // Add Member 
    // let memberIdx = $('#id_members-TOTAL_FORMS').val(); 

    // $('#addMember').click(function() {
    //     let lastRow = $('#member-container .member-row:last');
    //     let nameInput = lastRow.find('input[type="text"][name$="member_name"]');
    //     if (nameInput.val().trim() === "") { 
    //         alert("Please fill the current member before adding a new one."); 
    //         nameInput.focus(); 
    //         return; 
    //     }
    //     let newRow = lastRow.clone();
    //     newRow.find('input,select,textarea').each(function () {
    //         let name = $(this).attr('name');
    //         if (name) {
    //             name = name.replace(/-\d+-/, '-' + memberIdx + '-');
    //             $(this).attr('name', name);
    //         }
    //         let id = $(this).attr('id');
    //         if (id) {
    //             id = id.replace(/-\d+-/, '-' + memberIdx + '-');
    //             $(this).attr('id', id);
    //         }
    //         if ($(this).is(':radio') || $(this).is(':checkbox')) {
    //             $(this).prop('checked', false);
    //         } else {
    //             $(this).val('');
    //         }
    //     });
    //     newRow.find('.removeMember').show();
    //     $('#member-container').append(newRow);
    //     newRow.find('.member-wed').hide();
    //     memberIdx++;       
    //     $('#id_members-TOTAL_FORMS').val(memberIdx);
    // });

    // $('#member-container').on('click', '.removeMember', function() {
    //     $(this).closest('.member-row').remove();
    //     memberIdx--; 
    //     $('#id_members-TOTAL_FORMS').val(memberIdx);
    // });
    // $('.removeMember').hide();
    
});
// const memberrow = document.querySelectorAll('.member-row')
// console.log(memberrow)

// const radiobtn = document.querySelectorAll('input[type="radio"]');
// console.log(radiobtn);
// const member_wedDate = document.querySelector(".member-wed");
// console.log(member_wedDate)
// radiobtn.forEach(function(radio) {
//     radio.addEventListener('change', function() {
//         console.log(radio);
//         console.log(this.value);

//         if (this.value.toLowerCase() === "married"){
//             member_wedDate.style.display = 'block';
//         } else {
//             member_wedDate.style.display = 'none';
//         }
//     }) 
// });

// if (name) {
//                 name = name.replace(/-\\d+-/, '-' + memberIdx + '-');
//                 $(this).attr('name', name);
//             }
//             let id = $(this).attr('id');
//             if (id) {
//                 id = id.replace(/-\\d+-/, '-' + memberIdx + '-');
//                 $(this).attr('id', id);
//             }
//             if ($(this).is(':radio') || $(this).is(':checkbox')) {
//                 $(this).prop('checked', false);
//             } else {
//                 $(this).val('');
//             }


