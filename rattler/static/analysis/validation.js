$(function () {

    $('#analyseAuswahlForm').validate({
        rules:{
            resamplingScale:{
                maxlength:1,
                number:true,
            },
            hochpassCofreq:{
                number:true,
            },
            hochpassOrder:{
                number:true,
                maxlength:2,
            },
            tiefpassOrder:{
                number:true,
                maxlength:5,
            },
            tiefpassCofreq:{
                number:true,
            },
            gaussStd:{
                number:true,
                maxlength:2,
            },
            gaussM:{
                number:true,
                maxlength:5,

            },

        },

        messages: {
            resamplingScale: {
                maxlength:'Die Skalierung ist prozentual anzugeben: <br> 1 ~ 100% -> Deine Angabe ist zu groß.',
                number:'Bitte nur Zahlen eingeben.',
            },
            hochpassCofreq: {
                number:'Bitte nur Zahlen eingeben.',
            },
            hochpassOrder: {
                number:'Bitte nur Zahlen eingeben.',
                maxlength:'Diese Ordnung ist zu groß.',
            },
            tiefpassOrder: {
                number:'Bitte nur Zahlen eingeben.',
                maxlength:'Diese Ordnung ist zu groß.',
            },
            tiefpassCofreq: {
                number:'Bitte nur Zahlen eingeben.',
            },
            gaussStd: {
                number:'Bitte nur Zahlen eingeben.',
                maxlength:'Diese Ordnung ist zu groß.',
            },
            gaussM: {
                number:'Bitte nur Zahlen eingeben.',
                maxlength:'Diese Ordnung ist zu groß.',
            },
        },
            errorElement : "div",
         errorPlacement: function(error, element) {
          var placement = $(element).data('error');
          if (placement) {
            $(placement).append(error)
          } else {
            error.insertAfter(element);
          }},
    });
})