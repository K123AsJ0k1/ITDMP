import '../App.css'

const Result = ({data}) => {
    //console.log(data)
    return (
        <div className='result'>
            {data.status}
        </div>
    )
}

export default Result