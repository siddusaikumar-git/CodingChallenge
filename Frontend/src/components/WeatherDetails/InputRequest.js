import classes from "./InputRequest.module.css";
import { Fragment, useState } from "react";
import useInput from "../hooks/use-input";
import { ThreeCircles } from "react-loader-spinner";
import WeatherDetailList from "./WeatherDetailList";

function InputRequest() {
  const [spinner, setSpinner] = useState(false);
  const [weatherStats, setWeatherStats] = useState(false);
  const [responseData, setResponseData] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  const {
    value: enteredYear,
    isValid: enteredYearIsValid,
    hasError: yearInputHasError,
    valueInputChangeHandler: yearChangeHandler,
    inputBlurHandler: yearBlurHandler,
    reset: resetYearInput,
  } = useInput(
    (value) =>
      !(
        value.trim() === "" ||
        (Number(value.trim()) >= 1985 && Number(value.trim()) <= 2014)
      )
  );

  const yearInputClass = yearInputHasError
    ? `${classes.input} ${classes.invalid}`
    : `${classes.input}`;

  const {
    value: enteredStationId,
    isValid: enteredStationIdIsValid,
    hasError: stationIdInputHasError,
    valueInputChangeHandler: stationIdChangeHandler,
    inputBlurHandler: stationIdBlurHandler,
    reset: resetStationIdInput,
  } = useInput(
    (value) => !(value.trim() === "" || value.trim().startsWith("USC"))
  );

  const stationIdInputClass = stationIdInputHasError
    ? `${classes.input} ${classes.invalid}`
    : `${classes.input}`;

  const onToggleHandler = () => {
    setWeatherStats(!weatherStats);
    setResponseData(null);
  };
  const onSubmitHandler = async () => {
    if (enteredYearIsValid || enteredStationIdIsValid) {
      alert("Invalid Input");
      return;
    }
    setSpinner(true);
    setResponseData(null);
    const url = weatherStats
      ? new URL("http://localhost:5000/api/weather/stats")
      : new URL("http://localhost:5000/api/weather");
    if (enteredYear) {
      url.searchParams.append("year", enteredYear);
    }
    if (enteredStationId) {
      url.searchParams.append("stationid", enteredStationId);
    }
    if (pageNumber) {
      url.searchParams.append("page", pageNumber);
    }

    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Something went wrong!");
    }

    const responseJson = await response.json();
    console.log(responseJson);
    setSpinner(false);
    setResponseData(responseJson);
    resetYearInput();
    resetStationIdInput();
  };

  const prevPageButtonHandler = async () => {
    setSpinner(true);
    const url = responseData["prevLink"];
    setResponseData(null);
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Something went wrong!");
    }
    setPageNumber(pageNumber - 1);
    const responseJson = await response.json();
    setSpinner(false);
    setResponseData(responseJson);
  };

  const nextPageButtonHandler = async () => {
    setSpinner(true);
    const url = responseData["nextLink"];
    setResponseData(null);
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Something went wrong!");
    }
    setPageNumber(pageNumber + 1);
    const responseJson = await response.json();
    setSpinner(false);
    setResponseData(responseJson);
  };

  return (
    <Fragment>
      <div className={classes.input_title}>
        {!weatherStats && <h2>You are searching for Weather Data</h2>}
        {weatherStats && <h2>You are searching for Weather Stats</h2>}
        <button className={classes.button} onClick={onToggleHandler}>
          {!weatherStats && <span>Change to Weather Stats</span>}
          {weatherStats && <span>Change to Weather Data</span>}
        </button>
      </div>
      <div className={classes.input_request}>
        <div className={classes.year}>
          <label htmlFor="year" className={classes.label} />
          <div className={classes.input_div}>
            <input
              type="number"
              id="year"
              onChange={yearChangeHandler}
              onBlur={yearBlurHandler}
              value={enteredYear}
              className={yearInputClass}
              placeholder="Enter Year (1985 to 2014)"
              required
            />
          </div>
        </div>
        <div className={classes.stationid}>
          <label htmlFor="stationId" className={classes.label} />
          <div className={classes.input_div}>
            <input
              type="text"
              id="stationId"
              onChange={stationIdChangeHandler}
              onBlur={stationIdBlurHandler}
              value={enteredStationId}
              className={stationIdInputClass}
              placeholder="Enter Station ID"
              required
            />
          </div>
        </div>
      </div>
      <button className={classes.button} onClick={onSubmitHandler}>
        Submit
      </button>
      {responseData && (
        <WeatherDetailList
          output={responseData["results"]}
          weatherStats={weatherStats}
        />
      )}

      {spinner && (
        <ThreeCircles
          height="100"
          width="100"
          color="#4fa94d"
          wrapperStyle={{}}
          wrapperClass={classes.spinner}
          visible={true}
          ariaLabel="three-circles-rotating"
          outerCircleColor=""
          innerCircleColor=""
          middleCircleColor=""
        />
      )}
      <div className={classes.page_buttons}>
        {responseData && responseData["prevLink"] && (
          <button
            className={`${classes.button} ${classes.prevLink}`}
            onClick={prevPageButtonHandler}
          >
            Prev
          </button>
        )}
        {responseData && responseData["nextLink"] && (
          <button
            className={`${classes.button} ${classes.nextLink}`}
            onClick={nextPageButtonHandler}
          >
            Next
          </button>
        )}
      </div>
      {responseData && (
        <p className={classes.pageNumber}>Page number: {pageNumber}</p>
      )}
    </Fragment>
  );
}

export default InputRequest;
