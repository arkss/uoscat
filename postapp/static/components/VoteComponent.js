const {
  Button,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Grid
} = window['material-ui'];

class VoteComponent extends React.Component {
  constructor(props){
    super(props);
    this.state={
      open: false,
      choices: choices,
      tmp: '',
      voting: cat_voting,
    }
  }
  handleVote_increase =(i)=>{
    let choices=this.state.choices;
    choices[i].count++;
    this.setState({choices:choices})
  }
  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };
  handleDelete =(idx)=>{
    let choices=this.state.choices.filter((e,i)=>{return i!==idx});
    this.setState({choices:choices});
  }
  handleNewName = (e)=>{
    e.preventDefault();
    const tmp=e.target.value;
    this.setState({tmp: tmp})
  }
  addNewName=()=>{
    const name=this.state.tmp;
    const type=this.naming_error(name)
    if(type>0){
      var formdata=new FormData();
      formdata.set('add_name',name);
      axios({
        method: 'post',
        url: add_url,
        data: formdata,
        config: { headers: {'Content-Type': 'multipart/form-data' }}
      })
      .then(()=>location.reload());
      //error check pass
    }else if(type===-1){
      alert('공백말고 입력 ㄱ')
    }else if(type===-2){
      alert('이미 존재하는 이름')
    }
  }
  naming_error=(name)=>{
    if(name.trim().length<=0)return -1;
    const find=this.state.choices.filter(e=>{return e.name===name});
    if(find.length>0)return -2;
    return 1;
  }
  toggleVote=()=>{
    let nextVoting=this.state.voting;
    nextVoting=!nextVoting;
    axios({
      method: 'get',
      url: condition_url, //detail.html script
    }).then(()=>{
      this.setState({
        voting: nextVoting
      })
    })
  }

  render() {
    return (
      <div>
        {this.state.voting?(
          <Button variant="outlined" color="primary" onClick={this.handleClickOpen} style={{width: "100%"}}>
            이름 지어주기
          </Button>
          ):(
            <Button variant="outlined" color="primary" onClick={this.toggleVote} style={{width: "100%"}}>
              투표시작!
            </Button>
          )}

        <Dialog
          open={this.state.open}
          onClose={this.handleClose}
          aria-labelledby="form-dialog-title">
          <DialogTitle id="form-dialog-title">이름 투표 및 등록 진행중...</DialogTitle>
          <DialogContent>
            <Board choices={this.state.choices} handleVote_increase={this.handleVote_increase} handleDelete={this.handleDelete}/>
            <Grid container spacing={12}>
              <Grid item xs={9}>
              <TextField autoFocus margin="auto" id="newname_input" label="새이름 추가하기"
                type="text" onChange={this.handleNewName} style={{width:"100%"}} />
              </Grid>
              <Grid item xs>
                <Button onClick={this.addNewName} color="primary" style={{marginTop: "15px",marginLeft: "10px"}}>
                  등록
                </Button>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary">
              Cancel
            </Button>
            <Button onClick={()=>{this.handleClose();this.toggleVote()}} color="primary">
              투표종료
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

ReactDOM.render(<VoteComponent/>, document.getElementById('app'))
