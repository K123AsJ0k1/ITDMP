import { useState } from 'react'
import api from '../services/api'

const Form = () => {
  const [text, setText] = useState('')

  const checkText = (event) => {
    event.preventDefault()
    api.sendData({ text: text }).then(data => {
        console.log(data)
    })
  }

  return(
    <div>
      <h2>Check text with model</h2>
      <form onSubmit={checkText}>
        <div>
          text:
          <input
            id="text"
            type="text"
            value={text}
            name="text"
            onChange={({ target }) => setText(target.value)}
            placeholder='text'
          />
        </div>
        <button id="create-button" type="submit">Check text</button>
      </form>
    </div>
  )
}

export default Form
