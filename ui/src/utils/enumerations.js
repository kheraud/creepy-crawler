const RepositoryStatus = {
  0: {
    label: "To analyze",
    color: "grey lighten-3",
  },
  1: {
    label: "To test",
    color: "amber lighten-2",
  },
  2: {
    label: "Dropped",
    color: "brown darken-3",
  },
  3: {
    label: "To implement",
    color: "amber darken-3",
  },
  4: {
    label: "Implemented",
    color: "light-green lighten-2",
  }
};


const SelectRepositoryStatus = Object.entries(RepositoryStatus).map((x) => {
  return {
    value: +x[0],
    text: x[1].label,
  };
});


const SelectRepositorySort = [
  { text: "# Stars", value: 'stars' },
  { text: "# Forks", value: 'forks' },
  { text: "# Issues", value: 'issues' },
  { text: "Status", value: 'status' },
];

const RepositoryPerPage = 40;

export {
  SelectRepositorySort,
  RepositoryStatus,
  SelectRepositoryStatus,
  RepositoryPerPage,
};