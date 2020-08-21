const random = require('./random')

// random-date-generator:1.0.2 (package.json)
//let DateGenerator = require('random-date-generator');
//DateGenerator.getRandomDate(); // random date

/*
let startDate = new Date(2019,12,12);
let endDate = new Date(2020, 8, 8);
DateGenerator.getRandomDateInRange(startDate, endDate);
*/

const fake = {
  createData () {
    let deviceTypes = ["FS-15", "LF-10", "PP-5"];
    deviceId = Math.floor(Math.random() * 100);
    const data = {
      device: "device-" + deviceId,
      group: "group-" + deviceId % 10,
      devicetype: deviceTypes[deviceId % 3],
      date: DateGenerator.getRandomDate(),
      inputcurrent: Math.floor(850 + Math.random() * 100),
      inputcurrentunit: "amp",
      inputvoltage: Math.floor(210 + Math.random() * 20),
      inputvoltageunit: "ac-v",
      temp1: Math.floor(45 + Math.random() * 10),
      temp1unit: "c",
      temp2: Math.floor(25 + Math.random() * 10),
      temp2unit: "c",
      scale1: Math.floor(35 + Math.random() * 10),
      scale1unit: "kg",
      scale2: Math.floor(12 + Math.random() * 5),
      scale2unit: "kg",
      flow: Math.floor(40 + Math.random() * 10),
      flowunit: "m3/h"
    }
    return data
  }
}

module.exports = fake


