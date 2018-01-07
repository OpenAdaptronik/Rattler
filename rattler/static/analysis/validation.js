$(function () {

    $('#analyseAuswahlForm').validate({
        rules:{
            resamplingScale:{
                min:0.0001,
                max:10,
                number:true,
            },
            hochpassCofreq:{
                number:true,
            },
            hochpassOrder:{
                number:true,
                min:1,
                max:8,
            },
            tiefpassOrder:{
                number:true,
                min:1,
                max:8,
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
                min:'Die Skalierung ist prozentual anzugeben: <br> 1 ~ 100% -> Deine Angabe ist zu klein.',
                max:'Die Skalierung ist prozentual anzugeben: <br> 1 ~ 100% -> Deine Angabe ist zu groß.',
                number:'Bitte nur Zahlen eingeben.',
            },
            hochpassCofreq: {
                number:'Bitte nur Zahlen eingeben.',
            },
            hochpassOrder: {
                number:'Bitte nur Zahlen eingeben.',
                min:'Rang 1-8 ist möglich',
                max:'Rang 1-8 ist möglich',
            },
            tiefpassOrder: {
                number:'Bitte nur Zahlen eingeben.',
                min:'nur Rang 1-8 ist möglich',
                max:'nur Rang 1-8 ist möglich',

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