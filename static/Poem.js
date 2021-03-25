class PoemComponent extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            poem_header: [],
            poem: [],
        };
    }

    getPoem() {
        let st = document.getElementById("seed_text").value;
        let pt = document.getElementById("poet").value;
        const apiUrl = `http://localhost:5000/getpoem?seed_text=${st}&poet=${pt}`;
        fetch(apiUrl)
        .then(response => response.json())
        .then(
            (result) => {
                this.setState({ poem_header: result.poem_header})
                this.setState({ poem: result.poem });
            }
        );
    }

    render() {
        return (
            <div>
                <h5 class="text-responsive">
                    <u>MH Poem Generator</u>
                </h5>
                <input
                    type="text"
                    name="seed_text"
                    id="seed_text"
                    class="text-responsive"
                    size="21"
                    placeholder="Enter seed text: 3 to 5 words"
                />
                <br />
                <br />
                <select name="poet" id="poet" class="text-responsive">
                    <option value="">-- Please choose a poet --</option>
                    <option value="erica">Erica Jong</option>
                    <option value="lavanya">Lavanya Nukavarapu</option>
                    <option value="erica_lavanya">Erica+Lavanya</option>
                </select>
                <br />
                <br />
                <button type="button" class="btn btn-primary text-responsive" onClick={() => this.getPoem()}>
                    Generate Poem
                </button>
                <div id="generated_poem_header">
                    {this.state.poem_header.map(line => <div>{line}</div>)}
                </div>
                <div id="generated_poem">
                    {this.state.poem.map(line => <div>{line}</div>)}
                </div>
            </div>
        );
    }
}

const domContainer = document.querySelector("#poem_container");
ReactDOM.render(<PoemComponent />, domContainer);