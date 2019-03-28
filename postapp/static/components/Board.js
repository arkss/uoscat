const {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  withStyles,
  Radio,
  SvgIcon
}=window['material-ui']

class Board extends React.Component{
  handleVote= (id,url,i)=>{
    // axios(url) post.
    var formdata=new FormData();
    formdata.set('choice',id);
    axios({
      method: 'post',
      url: url,
      data: formdata,
      config: { headers: {'Content-Type': 'multipart/form-data' }}
    });
    this.props.handleVote_increase(i);
    // console.log(id,url,formdata);
  }
  handleDelete_board= (url,i)=>{
    axios.get(url);
    // console.log(url);
    this.props.handleDelete(i);
  }
  render(){

    return(
      <Table style={{width: "500px"}}>
        <TableHead>
          <TableRow>
            <TableCell align="center">이름</TableCell>
            <TableCell align="center">투표수</TableCell>
            <TableCell align="center">지지하기</TableCell>
            <TableCell align="center"></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {this.props.choices.map((e,i)=>(
            <TableRow>
              <TableCell align="center">{e.name}</TableCell>
              <TableCell align="center">{e.count}</TableCell>
              <TableCell align="center"><Radio onClick={()=>this.handleVote(e.id,e.vote_url,i)}/></TableCell>
              <TableCell align="center">
                <SvgIcon onClick={()=>this.handleDelete_board(e.delete_url,i)}>
                  <path d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z" />
                </SvgIcon>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    );
  }
}
