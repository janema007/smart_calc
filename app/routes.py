from app import app
from flask import render_template, request, url_for, redirect, session
from app.calculator import get_results


@app.route('/', methods=['GET', 'POST'])
def signin():
    try:
        if request.method == 'POST':
            return redirect(url_for("calculator"))
        return render_template("welcome.html")
    except ValueError:
        return render_template("error.html", error=ValueError)


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    try:
        if request.method == 'POST':

            render_template('calculator.html')
            origin = request.form.get("fromOrigin")
            destination = request.form.get("toDestination2")
            modeTransports = []
            returnBool = False
            clientTripBool = False
            wfhtime = 0
            originClient = 'Malmo'
            destinationClient = 'Croydon'


            if request.form.get("OneWayJourney") == "OneWayOption":
                returnBool = False
            if request.form.get("OneWayJourney") == "returnOption":
                returnBool = True
            if request.form.get("onewayDateStart"):
                dateDepartureOneWay = request.form.get("onewayDateStart")
            if request.form.get("oneWayDateEnd"):
                dateArrivalOneWay = request.form.get("oneWayDateEnd")
            if request.form.get("returnDateStart"):
                dateDepartureReturn = request.form.get("returnDateEnd")
            if request.form.get("returnDateEnd"):
                dateArrivalReturn = request.form.get("goingtoOffice")

            if request.form.get("goingtoOffice"):
                officetime = request.form.get("goingtoOffice")
            else:
                officetime = 0
            if request.form.get("goingtoClient"):
                clienttime = request.form.get("goingtoClient")
            else:
                clienttime = 0
            if request.form.get("wfh"):
                wfhtime = request.form.get("goingtoClient")
            else:
                wfhtime = 0
            if request.form.get("checkTrain"):
                modeTransports.append(request.form.get("checkTrain"))
            if request.form.get("checkBus"):
                modeTransports.append(request.form.get("checkBus"))
            if request.form.get("checkCar"):
                modeTransports.append(request.form.get("checkCar"))
            if request.form.get("checkWalking"):
                modeTransports.append(request.form.get("checkWalking"))
            if request.form.get("checkBicycle"):
                modeTransports.append(request.form.get("checkBicycle"))
            if request.form.get("hotelYes") == "hotelYes":
                clientTripBool = True
                originClient = request.form.get("fromOriginHotel")
                destinationClient = request.form.get("toDestinationHotel")

            if request.form.get("hotelYes") == "hotelNo":
                clientTripBool = False
                originClient = 'Malmo'
                destinationClient = 'Croydon'

            kwargs = {'origin': origin,
                      'destination':destination,
                      'dateDepartureOneWay':dateDepartureOneWay,
                      'dateArrivalOneWay':dateArrivalOneWay,
                      'dateDepartureReturn':dateDepartureReturn,
                      'dateArrivalReturn':dateDepartureReturn,
                      'returnBool':returnBool,
                      'officetime':officetime,
                      'clienttime':clienttime,
                      'wfhtime':wfhtime,
                      'modeTransports':modeTransports,
                      'clientTripBool':clientTripBool,
                      'originClient':originClient,
                      'destinationClient':destinationClient
                      }
            session['dict'] = kwargs
            return redirect(url_for("results"))

        return render_template("calculator.html")

    except ValueError:
        return render_template("error.html", error=ValueError)

@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        data = session['dict']
        results =  get_results(**data)
        return render_template('results.html',
                        distanceDriving=results['driving']['distance'],
                        emissionDriving=results['driving']['emissions'],
                        timeDriving=results['driving']['time'],
                        distanceTrain=results['transit_train']['distance'],
                        emissionTrain=results['transit_train']['emissions'],
                        timeTrain=results['transit_train']['time'],
                        distanceBus=results['transit_bus']['distance'],
                        emissionBus=results['transit_bus']['emissions'],
                        timeBus = results['transit_bus']['time'],
                        distanceBi=results['cycling']['distance'],
                        emissionBi = results['cycling']['emissions'],
                        timeBi=results['cycling']['time']

                        )
    except ValueError:
        return render_template("error.html", error=ValueError)

@app.route('/about', methods=['GET', 'POST'])
def about():
    try:
        return render_template("about.html")

    except ValueError:
        return render_template("error.html", error=ValueError)