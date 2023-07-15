import React, { useState } from "react";
import Grid from "@mui/material/Grid";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import LogoImage from "assets/images/avatar.png";
import Navbar from "components/Navbar";
import Avatar from "@mui/material/Avatar";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import GridViewIcon from "@mui/icons-material/GridView";
import { Autocomplete } from "@mui/material";
import MDCard from "components/MDCard";
import MDInput from "components/MDInput";
import BrandingWatermarkIcon from "@mui/icons-material/BrandingWatermark";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";
import MDButton from "components/MDButton";
import AddIcon from "@mui/icons-material/Add";
import MDBadge from "components/MDBadge";
import LocalOfferIcon from "@mui/icons-material/LocalOffer";
import VisibilityIcon from "@mui/icons-material/Visibility";
import TagIcon from "@mui/icons-material/Tag";
import Card from "@mui/material/Card";
import DataTable from "components/DataTable";
import { InputAdornment } from "@mui/material";
import { IconButton } from "@mui/material";
import { Search } from "@mui/icons-material";
import { contract } from "services/Authentication.Services";
import Loader from "components/Loader";
import { notifySuccess } from "components/Messages";
import { notifyError } from "components/Messages";
import TextSnippetIcon from '@mui/icons-material/TextSnippet';


function getTimeDifference(timestamp) {
  let currentTimestamp = Math.floor(Date.now() / 1000); // Get current timestamp in seconds
  let timeDifference = currentTimestamp - timestamp; // Calculate time difference in seconds

  let days = Math.floor(timeDifference / (3600 * 24)); // Calculate days
  let hours = Math.floor((timeDifference % (3600 * 24)) / 3600); // Calculate remaining hours
  let minutes = Math.floor((timeDifference % 3600) / 60); // Calculate remaining minutes
  let seconds = timeDifference % 60; // Calculate remaining seconds

  if (days > 0) {
    return days + " days ago";
  } else if (hours > 0) {
    return hours + " hrs " + minutes + " mins ago";
  } else if (minutes > 0) {
    return minutes + " mins ago";
  } else {
    return seconds + " secs ago";
  }
}

const cardData = [
  {
    title: "Overview",
    firstBlockHeader: "ETH BALANCE",
    firstBlockData: (
      <MDBox display="flex" alignItems="center">
        <GridViewIcon />
        <MDTypography variant="button" color={"text"} ml={0.7}>
          0.00
        </MDTypography>
      </MDBox>
    ),
    secondBlockHeader: "ETH VALUE",
    secondBlockData: "$0.00",
    thirdBlockHeader: "TOKEN HOLIDINGS",
    thirdBlockData: (
      <MDBox
        sx={{
          display: "flex",
          width: "100%",
          alignItems: "center",
          gap: 1,
          mt: 1,
        }}
      >
        <MDBox sx={{ width: "90%" }}>
          <Autocomplete
            disableClearable
            options={["$280,910.96 (42 Token)", 1131313, 313131, 1313131]}
            size="small"
            sx={{ width: " 100%" }}
            fullWidth
            renderInput={(params) => <MDInput {...params} fullWidth />}
          />
        </MDBox>
        <MDBox
          sx={{
            backgroundColor: "#e2e2e2",
            width: "40px",
            height: "33px",
            borderRadius: "2px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <BrandingWatermarkIcon />
        </MDBox>
      </MDBox>
    ),
  },
  {
    title: "Overview",
    firstBlockHeader: "PRIVATE NAME TAGS",
    firstBlockData: (
      <MDButton
        sx={{
          border: "1px dashed black",
          borderRadius: "40px",
          height: "15px",
        }}
      >
        <AddIcon /> Add
      </MDButton>
    ),
    secondBlockHeader: "CONTRACT CREATORS",
    secondBlockData: (
      <span style={{ color: "#0d7ee2" }}>
        Apecoin Deployer at txn 0*2732774g
      </span>
    ),
    thirdBlockHeader: "TOKEN TRACKER",
    thirdBlockData: (
      <MDBox display="flex">
        <Avatar
          alt="Shiv"
          src={LogoImage}
          sx={{ width: 24, height: 24, mr: 0.5 }}
        />
        <span style={{ color: "#0d7ee2", marginTop: "3px" }}>
          ApeCoin (APE){" "}
        </span>
        <span style={{ color: "grey", marginTop: "3px" }}>(@$4.13) </span>
      </MDBox>
    ),
  },
  {
    title: "Overview",
    firstBlockHeader: "PRIVATE NAME TAGS",
    firstBlockData: (
      <MDButton
        sx={{
          border: "1px dashed black",
          borderRadius: "40px",
          height: "15px",
        }}
      >
        <AddIcon /> Add
      </MDButton>
    ),
    secondBlockHeader: "CONTRACT CREATORS",
    secondBlockData: (
      <span style={{ color: "#0d7ee2" }}>
        Apecoin Deployer at txn 0*2732774g
      </span>
    ),
    thirdBlockHeader: "TOKEN TRACKER",
    thirdBlockData: (
      <MDBox display="flex">
        <Avatar
          alt="Shiv"
          src={LogoImage}
          sx={{ width: 24, height: 24, mr: 0.5 }}
        />
        <span style={{ color: "#0d7ee2", marginTop: "3px" }}>
          ApeCoin (APE){" "}
        </span>
        <span style={{ color: "grey", marginTop: "3px" }}>(@$4.13) </span>
      </MDBox>
    ),
  },
];
function Dashboard() {
  const [address, setAddress] = useState("");
  // const [, setContractIDData] = useState([])
  const [data, setData] = useState({})
  const [selectedTable, setSelectedTable] = useState("transaction")
  const [loading, setLoading] = useState(false);

  const fetchContract = async () => {
    try {
      setLoading(true);
      const response = await contract({ hex_address: address });
      const jsonBCData = response.data;
      setData({
        transaction: jsonBCData["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48_txn.json"],
        "internal-transaction": jsonBCData["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48_int_txn.json"],
        "erc20": jsonBCData["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48_erc20_add.json"],
        "erc20Contract": jsonBCData["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48_erc20_contract.json"],
        "events": jsonBCData["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48_log.json"],
        "nft-transfer": jsonBCData["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48_erc721_add.json"]
      });

      setLoading(false);
      // setContractIDData(jsonBCData)
      notifySuccess("Data Loaded Successfully");
    } catch (err) {
      setLoading(false);
      notifyError("Something went wrong");
      console.log(err);
    }
  };
  const transactionColumns = [
    {
      Header: <HelpOutlineIcon fontSize="small" />,
      accessor: "gas",
      Cell: (props) => {

        return (
          <MDBadge badgeContent={<VisibilityIcon />} color="light" container />
        );
      },
    },
    {
      Header: "Transaction Hash",
      accessor: "blockHash",
      Cell: (props) => {

        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.blockHash ?? "-"}
          </span>
        );
      },
    },
    {
      Header: (
        <MDBox
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <span>Method</span>
          <MDBox>
            <HelpOutlineIcon fontSize="small" />
          </MDBox>
        </MDBox>
      ),
      accessor: "blockNumber",
      Cell: (props) => {
        return (
          <MDBadge
            badgeContent="Transfer"
            color="light"
            container
            sx={{ mr: 1, mt: 1, fontSize: "5px" }}
          />
        );
      },
    },
    {
      Header: "Block",
      accessor: "cumulativeGasUsed",
      Cell: (props) => {
        return  props.row.original.blockNumber
      },
    },
    {
      Header: <span style={{ color: "#0d7ee2", fontSize: "14px" }}>Age</span>,
      accessor: "timeStamp",
      Cell: (props) => {
        return <>{getTimeDifference(props.row.original.timeStamp)}</>;
      },
    },
    {
      Header: "From",
      accessor: "from",
      Cell: (props) => {
        return (
          <MDBox
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 1,
            }}
          >
            <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
              {props.row.original.from ?? "-"}
            </span>

            <MDBox>
              <ContentCopyIcon sx={{ mt: 1 }} />
            </MDBox>
            <MDBadge badgeContent="IN" color="success" container />
          </MDBox>
        );
      },
    },
    {
      Header: "To",
      accessor: "to",
      Cell: (props) => {
        return (
          <MDBox
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 1,
            }}
          >
            <MDTypography sx={{ fontSize: "14px" }}>
              Center:USD Coin
            </MDTypography>
            <MDBox>
              <ContentCopyIcon sx={{ mt: 1 }} />
            </MDBox>
          </MDBox>
        );
      },
    },
    {
      Header: "Value",
      accessor: "value",
      Cell: (props) => {
        return `${props.row.original.value} ETH`;
      },
    },
    {
      Header: (
        <span style={{ color: "#0d7ee2", fontSize: "14px" }}>Txn Fee</span>
      ),
      accessor: "transactionIndex",
      Cell: (props) => {
        return props.row.original.gasPrice;
      },
    },
  ];

  const internalTransactions = [
    {
      Header: "Parent Txn Hash",
      accessor: "hash",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.hash ?? "-"}
          </span>
        );
      },
    },
    {
      Header: "Block",
      accessor: "blockNumber",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.blockNumber ?? "-"}
          </span>
        );
      },
    },
    {
      Header: <span style={{ color: "#0d7ee2", fontSize: "14px" }}>Age</span>,
      accessor: "timeStamp",
      Cell: (props) => {
        return <>{getTimeDifference(props.row.original.timeStamp)}</>;
      },
    },
    {
      Header: "From",
      accessor: "from",
      Cell: (props) => {
        return (
          <MDBox
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 1,
            }}
          >
            <MDBox>
              <TextSnippetIcon sx={{ mt: 1 }} />
            </MDBox>
            <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
              {props.row.original.from ?? "-"}
            </span>

            <MDBox>
              <ContentCopyIcon sx={{ mt: 1 }} />
            </MDBox>

          </MDBox>
        );
      },
    },
    {
      Header: "To",
      accessor: "gas",
      Cell: (props) => {
        return (
          <MDBox
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 1,
            }}
          >
            <MDBox>
              <TextSnippetIcon sx={{ mt: 1 }} />
            </MDBox>
            <MDTypography sx={{ fontSize: "14px" }}>
              Center:USD Coin
            </MDTypography>

            <MDBox>
              <ContentCopyIcon sx={{ mt: 1 }} />
            </MDBox>

          </MDBox>
        );
      },
    },
    {
      Header: "Value",
      accessor: "value",
      Cell: (props) => {
        return `${props.row.original.value} ETH`;
      },
    },
  ]

  const tokenTransferERC20 = [
    {
      Header: "Txn Hash",
      accessor: "hash",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.hash ?? "-"}
          </span>
        );
      },
    },
    {
      Header: "Method",
      accessor: "method",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.blockNumber ?? "-"}
          </span>
        );
      },
    },
    {
      Header: <span style={{ color: "#0d7ee2", fontSize: "14px" }}>Age</span>,
      accessor: "timeStamp",
      Cell: (props) => {
        return <>{getTimeDifference(props.row.original.timeStamp)}</>;
      },
    },
    {
      Header: "From",
      accessor: "from",
      Cell: (props) => {
        return (
          <MDBox
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 1,
            }}
          >
            <MDBox>
              <TextSnippetIcon sx={{ mt: 1 }} />
            </MDBox>
            <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
              {props.row.original.from ?? "-"}
            </span>

            <MDBox>
              <ContentCopyIcon sx={{ mt: 1 }} />
            </MDBox>

          </MDBox>
        );
      },
    },
    {
      Header: "To",
      accessor: "to",
    },
    {
      Header: "Value",
      accessor: "value",
      Cell: (props) => {
        return `${props.row.original.value} ETH`;
      },
    },
  ]

  const tokenTransferERC20Contract = [
    {
      Header: "Txn Hash",
      accessor: "hash",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.hash ?? "-"}
          </span>
        );
      },
    },
    {
      Header: "Method",
      accessor: "method",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.blockNumber ?? "-"}
          </span>
        );
      },
    },
    {
      Header: <span style={{ color: "#0d7ee2", fontSize: "14px" }}>Age</span>,
      accessor: "timeStamp",
      Cell: (props) => {
        return <>{getTimeDifference(props.row.original.timeStamp)}</>;
      },
    },
    {
      Header: "From",
      accessor: "from",
      Cell: (props) => {
        return (
          <MDBox
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 1,
            }}
          >
            <MDBox>
              <TextSnippetIcon sx={{ mt: 1 }} />
            </MDBox>
            <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
              {props.row.original.from ?? "-"}
            </span>

            <MDBox>
              <ContentCopyIcon sx={{ mt: 1 }} />
            </MDBox>

          </MDBox>
        );
      },
    },
    {
      Header: "To",
      accessor: "to",
    },
    {
      Header: "Value",
      accessor: "value",
      Cell: (props) => {
        return `${props.row.original.value} ETH`;
      },
    },
  ]

  const nftTransfer = [
    {
      Header: "Transaction Info",
      accessor: "hash",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.hash ?? "-"}
          </span>
        );
      },
    },
    {
      Header: "Method",
      accessor: "method",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.blockNumber ?? "-"}
          </span>
        );
      },
    },
    {
      Header: <span style={{ color: "#0d7ee2", fontSize: "14px" }}>Age</span>,
      accessor: "timeStamp",
      Cell: (props) => {
        return <>{getTimeDifference(props.row.original.timeStamp)}</>;
      },
    },
    {
      Header: "From",
      accessor: "from",
      Cell: (props) => {
        return (
          <MDBox
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 1,
            }}
          >
            <MDBox>
              <TextSnippetIcon sx={{ mt: 1 }} />
            </MDBox>
            <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
              {props.row.original.from ?? "-"}
            </span>

            <MDBox>
              <ContentCopyIcon sx={{ mt: 1 }} />
            </MDBox>

          </MDBox>
        );
      },
    },
    {
      Header: "To",
      accessor: "to",
    },
    {
      Header: "Type",
      Cell: (props) => {
        return `ERC 721`;
      },
    },
    {
      Header: "Item",
      Cell: (props) => {
        return props.row.original.tokenSymbol
      },
    },
  ]

  const events = [
    {
      Header: "Txn Hash",
      accessor: "transactionHash",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.transactionHash ?? "-"}
          </span>
        );
      },
    },
    {
      Header: "Block",
      accessor: "block",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.blockNumber ?? "-"}
          </span>
        );
      },
    },
    {
      Header: "Method",
      accessor: "method",
      Cell: (props) => {
        return (
          <span style={{ color: "#0d7ee2", fontSize: "14px" }}>
            {props.row.original.blockNumber ?? "-"}
          </span>
        );
      },
    },
    {
      Header: <span style={{ color: "#0d7ee2", fontSize: "14px" }}>Age</span>,
      accessor: "timeStamp",
      Cell: (props) => {
        return <>{getTimeDifference(props.row.original.timeStamp)}</>;
      },
    },
    {
      Header: "Logs",
      accessor: "logs",
      Cell: (props) => {
        return <div>
          {props.row.original.topics.map((i, idx) => {
            return <div>{`[topic${idx}] ${i}  `}</div>
          })}
        </div>
      },
    },
  ]

  const showColumns = () => {
    switch (selectedTable) {
      case "transactions":
        return transactionColumns;
      case "internal-transaction":
        return internalTransactions;
      case "events":
        return events
      case "erc20":
        return tokenTransferERC20
      case "erc20Contract":
        return tokenTransferERC20Contract
      case "nft-transfer":
        return nftTransfer;
      default:
        return transactionColumns;
    }

  }
  return (
    <React.Fragment>
      <Navbar />
        <Grid sx={{ backgroundColor: "#eaeaea" }}>
          <Grid>
            <MDTypography
              variant="h3"
              lineHeight={1}
              sx={{ cursor: "pointer", py: 2, pl: 2 }}
            >
              Ethereum Blockchain Explorer
            </MDTypography>
          </Grid>
          <Grid>
            <MDBox width="35rem">
              <MDInput
                sx={{ cursor: "pointer", py: 2, pl: 2 }}
                value={address}
                onChange={({ currentTarget }) =>
                  setAddress(currentTarget.value)
                }
                fullWidth
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        aria-label="toggle password visibility"
                        onClick={fetchContract}
                        edge="end"
                      >
                        <Search />
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />
              {loading ? <Loader /> : null}
            </MDBox>
          </Grid>
        </Grid>
      {true && (
        <>
          {" "}
          <Grid sx={{ backgroundColor: "#eaeaea" }}>
            <MDTypography
              variant="body1"
              lineHeight={1}
              sx={{ cursor: "pointer", py: 2, pl: 2 }}
            >
              UserId
            </MDTypography>
          </Grid>
          <Grid sx={{ borderBottom: "1px solid #e9e9f5", pb: 1.5 }}>
            <MDBox sx={{ display: "flex", mt: 1, pl: 2 }}>
              <MDBox display="flex">
                <Avatar
                  alt="Shiv"
                  src={LogoImage}
                  sx={{ width: 24, height: 24 }}
                />
                <MDTypography variant="h5" sx={{ ml: 1, mr: 1 }}>
                  Contract
                </MDTypography>
              </MDBox>
              <span style={{ marginTop: "6px", marginRight: "11px" }}>
                {address}
              </span>
              <ContentCopyIcon sx={{ mt: 1 }} />
              <GridViewIcon sx={{ mt: 1, ml: 1 }} />
            </MDBox>
          </Grid>
          <Grid sx={{ pb: 1.5 }}>
            <MDBox sx={{ display: "flex", mt: 1, pl: 2 }}>
              <MDBox display="flex">
                <span style={{ marginTop: "10px", marginRight: "1px" }}>
                  SALES! Get 15% off(one-time) for any new API Pro Subscription.
                </span>
                <MDTypography
                  variant="h6"
                  sx={{ ml: 0.5, mr: 1, mt: 0.8, color: "#0d7ee2" }}
                >
                  Code:ESFP15Q223
                </MDTypography>
              </MDBox>
            </MDBox>
          </Grid>
        </>
      )}
      <Grid sx={{ pb: 1.5 }}>
        <MDBox sx={{ pl: 2 }}>
          <MDButton
            color="light"
            sx={{ borderRadius: 10, border: "1px solid #abadb1", mt: 1, mr: 1 }}
          >
            <LocalOfferIcon sx={{ mr: 1 }} /> Apecoin: APE Token{" "}
            <ContentCopyIcon sx={{ ml: 1 }} />
          </MDButton>
          <MDButton
            color="success"
            sx={{
              borderRadius: 10,
              border: "1px solid #abadb1",
              width: "150px",
              mt: 1,
              mr: 1,
            }}
          >
            Source Code
          </MDButton>
          <MDButton
            color="light"
            sx={{
              borderRadius: 10,
              border: "1px solid #abadb1",
              width: "200px",
              mt: 1,
              mr: 1,
            }}
          >
            <TagIcon sx={{ mr: 1 }} /> Token Contracts
          </MDButton>
        </MDBox>
      </Grid>

      {/* <Grid sx={{ borderBottom: "1px solid #e9e9f5", pb: 1.5 }}>
      <MDBox>
      </MDBox>
      <MDBox>
      </MDBox>
      </Grid> */}

      {/* Card Part here */}

      <MDBox mb={3}>
        <Grid container spacing={3}>
          {cardData?.map((item, index) => {
            return (
              <Grid item xs={12} lg={4} key={index}>
                <MDCard
                  title={item?.title}
                  firstBlockHeader={item?.firstBlockHeader}
                  firstBlockData={item?.firstBlockData}
                  secondBlockHeader={item?.secondBlockHeader}
                  secondBlockData={item?.secondBlockData}
                  thirdBlockHeader={item?.thirdBlockHeader}
                  thirdBlockData={item?.thirdBlockData}
                />
              </Grid>
            );
          })}
        </Grid>
      </MDBox>

      {true && (
        <>
          {" "}
          <Grid sx={{ borderBottom: "1px solid #e9e9f5", pb: 1.5 }}>
            <MDBox sx={{ pl: 2 }}>
              <MDBadge
                badgeContent="Transactions"
                size="md"
                container
                color={selectedTable === "transaction" ? null : "light"}
                sx={{ mr: 1, mt: 1 }}
                onClick={() => setSelectedTable('transaction')}
              />
              <MDBadge
                badgeContent="Internal Transactions"
                color={selectedTable === "internal-transaction" ? null : "light"}
                onClick={() => setSelectedTable('internal-transaction')}
                container
                sx={{ mr: 1, mt: 1, cursor: "pointer" }}
              />
              <MDBadge
                badgeContent="Token Transfer (ERC:20)"
                color={selectedTable === "erc20" ? null : "light"}
                container
                sx={{ mr: 1, mt: 1 }}
                onClick={() => setSelectedTable('erc20')}
              />
              <MDBadge
                badgeContent="NFT Transfer"
                color={selectedTable === "nft-transfer" ? null : "light"}
                container
                onClick={() => setSelectedTable('nft-transfer')}
                sx={{ mr: 1, mt: 1 }}
              />
              <MDBadge
                badgeContent="Token Transfer (ERC:20 Contract)"
                color={selectedTable === "erc20Contract" ? null : "light"}
                onClick={() => setSelectedTable('erc20Contract')}
                container
                sx={{ mr: 1, mt: 1 }}
              />
              <MDBadge
                badgeContent="Events"
                onClick={() => setSelectedTable('events')}
                color={selectedTable === "events" ? null : "light"}
                container
                sx={{ mr: 1, mt: 1 }}
              />
              <MDBadge
                badgeContent="Analaytics"
                color={"light"}
                container
                sx={{ mr: 1, mt: 1 }}
              />
              <MDBadge
                badgeContent="Info"
                color={selectedTable === "info" ? null : "light"}
                onClick={() => setSelectedTable('info')}
                container
                sx={{ mr: 1, mt: 1 }}
              />
              <MDBadge
                badgeContent="Comments"
                color={"light"}
                container
                sx={{ mr: 1, mt: 1 }}
              />
            </MDBox>
          </Grid>
          <MDBox mb={3}>
            <Card>
              {/* <MDBox p={3} lineHeight={1}>
                <MDTypography variant="button" color="text">
                  <ArrowDownwardIcon /> Latest 25 drom a total of
                  <span style={{ color: "#0d7ee2" }}>
                    {" "}
                    {jsonItems.length}
                  </span>{" "}
                  transcations
                </MDTypography>
                <MDBox>
                  <MDTypography variant="button" color="text">
                    (More than{" "}
                    <span style={{ color: "#0d7ee2" }}>25 Pending Txns</span>)
                  </MDTypography>
                </MDBox>
              </MDBox> */}

              {loading ? (
                <Loader />
              ) : selectedTable === 'info' ? <MDCard firstBlockHeader="OVERVIEW" firstBlockData="USDC is a fully collateralized US Dollar stablecoin developed by CENTRE, the open source project with Circle being the first of several forthcoming issuers.
              ">
              </MDCard> : (
                <DataTable table={{ columns: showColumns(), rows: data[selectedTable] ?? [] }} />

              )}
              {/* 
              <DataTable table={dataTableData} isLoading={false} /> */}
            </Card>
          </MDBox>
        </>
      )}

      {/* <Grid container>
        <SalesByCountry />
      </Grid> */}

      <MDBox mt={1.5}></MDBox>
      {/* <Footer /> */}
    </React.Fragment>
  );
}

export default Dashboard;
// erc20 contract:0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
// contract deployer: 0x95ba4cf87d6723ad9c0db21737d862be80e93911