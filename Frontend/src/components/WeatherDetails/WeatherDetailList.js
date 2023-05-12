import classes from "./WeatherDetailList.module.css";
import WeatherDetailItem from "./WeatherDetailItem";
import { Fragment } from "react";

function WeatherDetailList(props) {
  console.log(props);
  return (
    <Fragment>
      {props.weatherStats && (
        <ul className={classes.list}>
          {props.output.map((item) => (
            <WeatherDetailItem
              key={
                item.stationid +
                item.avg_maxtemp +
                item.avg_mintemp +
                item.total_precipitation
              }
              maxtemp={item["avg_maxtemp"]}
              mintemp={item["avg_mintemp"]}
              stationid={item.stationid}
              precipitation={item["total_precipitation"]}
              year={item.year}
              weatherStats={props.weatherStats}
            />
          ))}
        </ul>
      )}
      {!props.weatherStats && (
        <ul className={classes.list}>
          {props.output.map((item) => (
            <WeatherDetailItem
              key={
                item.stationid +
                item.maxtemp +
                item.mintemp +
                item.precipitation
              }
              maxtemp={item.maxtemp}
              mintemp={item.mintemp}
              stationid={item.stationid}
              precipitation={item.precipitation}
              year={item.year}
              date={item.date}
              weatherStats={props.weatherStats}
            />
          ))}
        </ul>
      )}
    </Fragment>
  );
}

export default WeatherDetailList;
