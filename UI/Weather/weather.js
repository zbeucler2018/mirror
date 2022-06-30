

const CITY = "Andover";
const STATE = "MA";
const COUNTRY = "US";

let weatherData;
let minutes_between_refreshes = 0.15;

function preload() {
    weatherData = getWeatherData();
}

function setup() {
	createCanvas(windowWidth, windowHeight);
    background("Black");
    noStroke();
    fill("White");
}

function getWeatherData() {
    let URL = "https://api.openweathermap.org/data/2.5/weather?q="+CITY+","+STATE+","+COUNTRY+"&appid=e7402cc176aacd446829a856f2723b57&units=imperial";
    return loadJSON(URL);
}


function draw(){  
    if (frameCount % (60*60*minutes_between_refreshes) == 0) {
        weatherData = getWeatherData();
    }

    if (weatherData.main != undefined) {
        let description = weatherData.weather[0].description;
        let current_temp = weatherData.main === undefined ? "" : weatherData.main.temp.toString();
        let feels_like = weatherData.main === undefined ? "" : weatherData.main.feels_like.toString();
        //let max_temp = weatherData.main.temp_max.toString();
        //let min_temp = weatherData.main.temp_min.toString();
        //let humidity = weatherData.main.humidity.toString();
        //let idk = weatherData.weather[0].main.toString();
        let icon = weatherData.main === undefined ? "" : weatherData.weather[0].icon;

        text(description, width/2, height/2);
        //text(Math.round(current_temp)+" °F",  width/2, (height/2)+30);
        //text(Math.round(feels_like)+" °F",  width/2, (height/2)+60);
        text(current_temp+" °F",  width/2, (height/2)+30);
        text(feels_like+" °F",  width/2, (height/2)+60);
        text(icon, width/2, (height/2)+90);
    }




}

/*      ICONS
- https://github.com/madzadev/weather-app/tree/main/public/icons
- weatherData.weather[0].icon
- https://www.iconsdb.com/white-icons/white-weather-icons.html

01d     sunny / clear sky
01n     nighttime sunny
02d
02n
03d     cloudy
03n     cloudy
04d     very cloudy
04n     very cloudy
09d     rainy
09n     rainy
10d     rainy
10n     rainy
11d     thunder storm
11n     thunder storm
13d     cloudy snow / blizzard?
13n     cloudy snow / blizzard?
50d     fog/mist
50n     fog/mist

d = day
n = night
*/