const EventEmitter = require('events')

const utils = require('./utils')
const random = require('./random')

class Eventer extends EventEmitter {
}

const eventer = new Eventer()

eventer.send = (event) =>
{
  const id = random.createString(16)
  const at = utils.createTimestamp()
  const output = {
    device: "device-0",
    group: "group-0",
    devicetype: "FS-15",
    date: "01-04-2018T00:0:00.000Z",
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

  eventer.emit('event', output)
}

module.exports = eventer
