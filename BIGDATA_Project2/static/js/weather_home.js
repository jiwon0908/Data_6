//First slide weather
$.simpleWeather({
    location: 'Seoul, Korea',
    woeid: '',
    unit: 'c',
    success: function(weather) {
      html = '<h6><i class="weathericon-'+weather.code+'"></i> '+weather.temp+'&deg;'+weather.units.temp+'</h6>';
  
      $("#weather").html(html);
    },
    error: function(error) {
      $("#weather").html('<p>'+error+'</p>');
    }
  });

//Second slide weather
 $.simpleWeather({
    location: 'Busan, Korea',
    woeid: '',
    unit: 'c',
    success: function(weather) {
      html = '<h6><i class="weathericon-'+weather.code+'"></i> '+weather.temp+'&deg;'+weather.units.temp+'</h6>';
  
      $("#weather_2").html(html);
    },
    error: function(error) {
      $("#weather_2").html('<p>'+error+'</p>');
    }
  });

//Third slide weather
 $.simpleWeather({
    location: 'Toyko, Japan',
    woeid: '',
    unit: 'c',
    success: function(weather) {
      html = '<h6><i class="weathericon-'+weather.code+'"></i> '+weather.temp+'&deg;'+weather.units.temp+'</h6>';
  
      $("#weather_3").html(html);
    },
    error: function(error) {
      $("#weather_3").html('<p>'+error+'</p>');
    }
  });

//Fourth slide weather
 $.simpleWeather({
    location: 'Washington D.C., United States',
    woeid: '',
    unit: 'c',
    success: function(weather) {
      html = '<h6><i class="weathericon-'+weather.code+'"></i> '+weather.temp+'&deg;'+weather.units.temp+'</h6>';
  
      $("#weather_4").html(html);
    },
    error: function(error) {
      $("#weather_4").html('<p>'+error+'</p>');
    }
  });

//fifth slide weather
 $.simpleWeather({
    location: 'Beijing, China',
    woeid: '',
    unit: 'c',
    success: function(weather) {
      html = '<h6><i class="weathericon-'+weather.code+'"></i> '+weather.temp+'&deg;'+weather.units.temp+'</h6>';
  
      $("#weather_5").html(html);
    },
    error: function(error) {
      $("#weather_5").html('<p>'+error+'</p>');
    }
  });