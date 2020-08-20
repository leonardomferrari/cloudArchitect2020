const random = require('./random')

const fake = {
  createData () {
    let deviceTypes = ["FS-15", "LF-10", "PP-5"];
    deviceId = Math.floor(Math.random());
    const data = {
      device: "device-" + deviceId,
      group: "group-" + deviceId % 10,
      devicetype: deviceTypes[deviceId % 3],
      date: new Date().toISOString(),
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
