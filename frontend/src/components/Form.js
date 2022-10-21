import { useState } from 'react'
import api from '../services/api'
import '../App.css'

const Form = ({setData}) => {
  const [text, setText] = useState('')

  const checkText = (event) => {
    event.preventDefault()
    api.sendData({ text: text }).then(data => {
        setData(data)
        //console.log(data)
    })
  }

  return(
    <div>
      <form onSubmit={checkText} className='form'>
        <button id="create-button" type="submit" className='formButton'>Copy your text and click this!</button>
        <div>
          <textarea
            id="text"
            type="text"
            value={text}
            name="text"
            onChange={({ target }) => setText(target.value)}
            className='formTextBox'
          />
        </div>
      </form>
    </div>
  )
}

export default Form
