import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { useTable, useSortBy } from "react-table";
import KeyboardDoubleArrowDownIcon from "@mui/icons-material/KeyboardDoubleArrowDown";
import KeyboardDoubleArrowUpIcon from "@mui/icons-material/KeyboardDoubleArrowUp";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import update from "immutability-helper";
import { DragIndicator } from "@mui/icons-material";
import "./index.css";

function DataTable({ columns, data }) {
  const [tableData, setTableData] = useState(data);
  console.log("table", tableData);

  const getRowId = React.useCallback((row) => {
    return row.id;
  }, []);

  const { getTableProps, headerGroups, rows, prepareRow } = useTable(
    {
      data: tableData,
      columns,
      getRowId,
    },
    useSortBy
  );

  useEffect(() => {
    setTableData(data);
  }, [data]);

  const moveRow = (dragIndex, hoverIndex) => {
    const dragRecord = tableData[dragIndex];
    setTableData(
      update(tableData, {
        $splice: [
          [dragIndex, 1],
          [hoverIndex, 0, dragRecord],
        ],
      })
    );
  };

  return (
    <DndProvider backend={HTML5Backend}>
      {/* <TableContainer sx={{ height: "600px" }}> */}
      <Table
        {...getTableProps()}
        sx={{ borderCollapse: "separate", borderSpacing: "0px 15px" }}
      >
        <TableHead sx={{ position: "sticky", top: 0, background: "white" }}>
          {headerGroups.map((headerGroup) => (
            <TableRow {...headerGroup.getHeaderGroupProps()}>
              <TableCell>Move</TableCell>
              {headerGroup.headers.map((column) => (
                <TableCell
                  {...column.getHeaderProps(column.getSortByToggleProps())}
                >
                  {column.render("Header")}
                  {column.isSorted ? (
                    column.isSortedDesc ? (
                      <KeyboardDoubleArrowDownIcon />
                    ) : (
                      <KeyboardDoubleArrowUpIcon />
                    )
                  ) : (
                    ""
                  )}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableHead>
        <TableBody sx={{ backgroundColor: "#f8f8f8" }}>
          {rows.map((row, index) => {
            return (
              prepareRow(row) || (
                <Row
                  index={index}
                  row={row}
                  moveRow={moveRow}
                  {...row.getRowProps()}
                />
              )
            );
          })}
        </TableBody>
      </Table>
      {/* </TableContainer> */}
    </DndProvider>
  );
}
const DND_ITEM_TYPE = "row";

const Row = ({ row, index, moveRow }) => {
  const dropRef = React.useRef(null);
  const dragRef = React.useRef(null);

  const [, drop] = useDrop({
    accept: DND_ITEM_TYPE,
    hover(item, monitor) {
      if (!dropRef.current) {
        return;
      }
      const dragIndex = item.index;
      const hoverIndex = index;
      // Don't replace items with themselves
      if (dragIndex === hoverIndex) {
        return;
      }
      // Determine rectangle on screen
      const hoverBoundingRect = dropRef.current.getBoundingClientRect();
      // Get vertical middle
      const hoverMiddleY =
        (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2;
      // Determine mouse position
      const clientOffset = monitor.getClientOffset();
      // Get pixels to the top
      const hoverClientY = clientOffset.y - hoverBoundingRect.top;
      // Only perform the move when the mouse has crossed half of the items height
      // When dragging downwards, only move when the cursor is below 50%
      // When dragging upwards, only move when the cursor is above 50%
      // Dragging downwards
      if (dragIndex < hoverIndex && hoverClientY < hoverMiddleY) {
        return;
      }
      // Dragging upwards
      if (dragIndex > hoverIndex && hoverClientY > hoverMiddleY) {
        return;
      }
      // Time to actually perform the action
      moveRow(dragIndex, hoverIndex);
      // Note: we're mutating the monitor item here!
      // Generally it's better to avoid mutations,
      // but it's good here for the sake of performance
      // to avoid expensive index searches.
      item.index = hoverIndex;
    },
  });

  const [{ isDragging }, drag, preview] = useDrag({
    type: DND_ITEM_TYPE,
    item: { type: DND_ITEM_TYPE, index },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  const opacity = isDragging ? 0 : 1;

  preview(drop(dropRef));
  drag(dragRef);

  return (
    <>
      <TableRow ref={dropRef} style={{ opacity }}>
        <TableCell
          ref={dragRef}
          sx={{
            "&::before": {
              background: "red",
            },
          }}
        >
          {" "}
          <DragIndicator
            sx={{ fontSize: 80, width: "25px", height: "25px", pl: 2 }}
            size="large"
          />
        </TableCell>
        {row.cells.map((cell) => {
          return (
            <TableCell {...cell.getCellProps()}>
              {cell.render("Cell")}
            </TableCell>
          );
        })}
      </TableRow>
    </>
  );
};

export default DataTable;
