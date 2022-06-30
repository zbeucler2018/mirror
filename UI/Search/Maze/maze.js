


function Cell(i, j) {
    this._col = i;
    this._row = j;
    this.walls = [true, true, true, true];
    this.visited = false;
  
    this.checkNeighbors = function() {
      var neighbors = [];
  
      var top = grid[index(this._col, this._row - 1)];
      var right = grid[index(this._col + 1, this._row)];
      var bottom = grid[index(this._col, this._row + 1)];
      var left = grid[index(this._col - 1, this._row)];
  
      if (top && !top.visited) {
        neighbors.push(top);
      }
      if (right && !right.visited) {
        neighbors.push(right);
      }
      if (bottom && !bottom.visited) {
        neighbors.push(bottom);
      }
      if (left && !left.visited) {
        neighbors.push(left);
      }
  
      if (neighbors.length > 0) {
        var r = floor(random(0, neighbors.length));
        return neighbors[r];
      } else {
        return undefined;
      }
  
  
    }
    this.highlight = function() {
      var x = this._col * CELL_SIZE;
      var y = this._row * CELL_SIZE;
      noStroke();
      fill(0, 0, 255, 100);
      rect(x, y, CELL_SIZE, CELL_SIZE);
  
    }
  
    this.show = function() {
      var x = this._col * CELL_SIZE;
      var y = this._row * CELL_SIZE;
      stroke(255);
      if (this.walls[0]) {
        line(x, y, x + CELL_SIZE, y);
      }
      if (this.walls[1]) {
        line(x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE);
      }
      if (this.walls[2]) {
        line(x + CELL_SIZE, y + CELL_SIZE, x, y + CELL_SIZE);
      }
      if (this.walls[3]) {
        line(x, y + CELL_SIZE, x, y);
      }
  
      if (this.visited) {
        noStroke();
        fill(255, 0, 255, 100);
        rect(x, y, CELL_SIZE, CELL_SIZE);
      }
    }
}





var TOTAL_COLS, TOTAL_ROWS;
var CELL_SIZE = 50;
var grid = [];

var current;

var stack = [];

function setup() {
  createCanvas(windowWidth, windowHeight);
  TOTAL_COLS = floor(width / CELL_SIZE);
  TOTAL_ROWS = floor(height / CELL_SIZE);
  //frameRate(5);

  for (var r = 0; r < TOTAL_ROWS; r++) {
    for (var c = 0; c < TOTAL_COLS; c++) {
      var cell = new Cell(c, r);
      grid.push(cell);
    }
  }

  current = grid[0];


}

function draw() {
  for (var i = 0; i < grid.length; i++) {
    grid[i].show();
  }
  current.visited = true;
  current.highlight(); // show the heads
  // STEP 1
  var next = current.checkNeighbors();
  if (next) {
    next.visited = true;
    // STEP 2
    stack.push(current);
    // STEP 3
    removeWalls(current, next);
    // STEP 4
    current = next;
  } else if (stack.length > 0) {
    current = stack.pop();
  }


  if (current === grid[0] && grid[0].visited) {
    console.log('Grid Generated')
  }

}

function index(i, j) {
  if (i < 0 || j < 0 || i > TOTAL_COLS - 1 || j > TOTAL_ROWS - 1) {
    return -1;
  }
  return i + j * TOTAL_COLS;
}


function removeWalls(a, b) {
  var x = a._col - b._col;
  if (x === 1) {
    a.walls[3] = false;
    b.walls[1] = false;
  } else if (x === -1) {
    a.walls[1] = false;
    b.walls[3] = false;
  }
  var y = a._row - b._row;
  if (y === 1) {
    a.walls[0] = false;
    b.walls[2] = false;
  } else if (y === -1) {
    a.walls[2] = false;
    b.walls[0] = false;
  }
}