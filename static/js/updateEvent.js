$(document).ready(function () {
    // toggle head wedding date 
    // $('#wedding_date').hide();
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
        // memberRow.find('.member-wed').hide();
        if ($(this).is(':checked') && $(this).val().toLowerCase() === "married") {
            memberRow.find('.member-wed').show();
        } else {
            memberRow.find('.member-wed').hide();
            memberRow.find('input[name$="member_wedDate"]').val('');
        }
    });

    // Add Hobby
    // let formIdx = {{ formset.total_form_count|add:"-1" }};
    let formIdx = $('#id_hobbies-TOTAL_FORMS').val(); 
    $('#addHobby').click(function() {
        let lastRow = $('#hobby-container .hobby-row:last');
        if (lastRow.length) {
            let nameInput = lastRow.find('input[type="text"]');;
            if (nameInput.val().trim() === "") {
                alert("Please fill the current member before adding a new one.");
                nameInput.focus();
                return;
            }
        }
        
        let newRow = $('#hobby-template .hobby-row').clone();
        newRow.find('input,div').each(function () {
            let name = $(this).attr('name');
            if (name) {
                name = name.replace(/__prefix__/, formIdx);
                $(this).attr('name', name);
            }
            let id = $(this).attr('id');
            if (id) {
                id = id.replace(/__prefix__/, formIdx);
                $(this).attr('id', id);
            }
        });
        $('#hobby-container').append(newRow);
        formIdx++;       
        $('#id_hobbies-TOTAL_FORMS').val(formIdx);
    });
    // Remove Hobby
    $('#hobby-container').on('click', '.removeHobby', function() {
        $(this).closest('.hobby-row').remove();
        formIdx--; 
        $('#id_form-TOTAL_FORMS').val(formIdx);
    });
    // $('.removeHobby').hide();

    // Add Member 
    let memberIdx = $('#id_members-TOTAL_FORMS').val(); 

    $('#addMember').click(function() {
        let lastRow = $('#member-container .member-row:last');
        if (lastRow.length) {
            let nameInput = lastRow.find('input[type="text"][name$="member_name"]');
            if (nameInput.val().trim() === "") {
                alert("Please fill the current member before adding a new one.");
                nameInput.focus();
                return;
            }
        }
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
        newRow.find('.mem_photDiv').html(`
        <label for="id_members-${memberIdx}-member_photo">Photo:</label>
        <input type="file" name="members-${memberIdx}-member_photo" accept="image/*" id="id_members-${memberIdx}-member_photo">
        <span class="errorMsg"></span>`);
        $('#member-container').append(newRow);
        newRow.find('.member-wed').hide();
        memberIdx++;
        $('#id_members-TOTAL_FORMS').val(memberIdx);
        // newRow.find('input[type="checkbox"][name$="member_photo-clear"]').remove();
        // newRow.find('a').remove();
        // newRow.find('label[for$="member_photo-clear_id"]').remove();
        // newRow.find('input[type="file"][name$="member_photo"]').val('')
    });

    function reindexMembers() {
        let rows = $('#member-container .member-row');
        rows.each(function (i, row) {
            $(row).find('input, select, textarea, label').each(function () {
                let name = $(this).attr('name');
                if (name) {
                    $(this).attr('name', name.replace(/members-\d+-/, 'members-' + i + '-'));
                }
                let id = $(this).attr('id');
                if (id) {
                    $(this).attr('id', id.replace(/members-\d+-/, 'members-' + i + '-'));
                }
                let labelfor = $(this).attr('for');
                if (labelfor) {
                    $(this).attr('for', labelfor.replace(/members-\d+-/, 'members-' + i + '-'));
                }
            });
        });
        $('#id_members-TOTAL_FORMS').val(rows.length);
    }
    // remove member
    $('#member-container').on('click', '.removeMember', function () {
        $(this).closest('.member-row').remove();
        reindexMembers(); 
        memberIdx--; 
        $('#id_members-TOTAL_FORMS').val(memberIdx);
    });
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

// $('#addHobby').click(function() {
    //     let lastInput = $('#hobby-container .hobby-row:last input[type="text"]'); 
    //     if (lastInput.val().trim() === "") { 
    //         alert("Please fill the current hobby before adding a new one."); 
    //         lastInput.focus(); 
    //         return; 
    //     }
    //     let lastRow = $('#hobby-container .hobby-row:last')
    //     let newRow = lastRow.clone();
    //     newRow.find('input').each(function() {
    //         let name = $(this).attr('name');
    //         if (name) {
    //             name = name.replace(/-\d+-/, '-' + formIdx + '-');
    //             $(this).attr('name', name);
    //         }
    //         let id = $(this).attr('id');
    //         if (id) {
    //             id = id.replace(/-\d+-/, '-' + formIdx + '-');
    //             $(this).attr('id', id);
    //         }
            
    //     });
    //     newRow.find('.removeHobby').show();
    //     $('#hobby-container').append(newRow);        formIdx++;       
    //     $('#id_hobbies-TOTAL_FORMS').val(formIdx);
    // });