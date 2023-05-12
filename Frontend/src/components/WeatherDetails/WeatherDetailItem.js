import Card from "../UI/Card";
import classes from "./WeatherDetailItem.module.css";

function WeatherDetailItem(props) {
  return (
    <Card>
      <li className={classes.item}>
        <div className={classes.content}>
          <p className={classes.label}>Year: </p>
          <p className={classes.value}>{props.year}</p>
          <p className={classes.label}>Station ID: </p>
          <p className={classes.value}>{props.stationid}</p>
          <p className={classes.label}>
            {props.weatherStats ? "AVG Max Temp:" : "Max Temp:"}
          </p>
          <p className={classes.value}>{props.maxtemp}</p>
          <p className={classes.label}>
            {props.weatherStats ? "AVG Min Temp:" : "Min Temp:"}
          </p>
          <p className={classes.value}>{props.mintemp}</p>
          <p className={classes.label}>
            {props.weatherStats ? "Total Precipitation:" : "Precipitation:"}
          </p>
          <p className={classes.value}>{props.precipitation}</p>
          {!props.weatherStats && <p className={classes.label}>Date: </p>}
          {!props.weatherStats && <p className={classes.value}>{props.date}</p>}
        </div>
      </li>
    </Card>
  );
}

export default WeatherDetailItem;
