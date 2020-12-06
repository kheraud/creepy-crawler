const RepositoryStatus = [
  {
    id: 0,
    label: "To analyze",
    color: "blue-grey darken-3",
    icon: "mdi-help-circle-outline",
  },
  {
    id: 1,
    label: "To test",
    color: "orange accent-4",
    icon: "mdi-flask-empty-outline",
  },
  {
    id: 2,
    label: "Dropped",
    color: "blue-grey lighten-3",
    icon: "mdi-minus-circle-outline",
  },
  {
    id: 3,
    label: "To implement",
    color: "deep-orange accent-3",
    icon: "mdi-shovel",
  },
  {
    id: 4,
    label: "Implemented",
    color: "green darken-3",
    icon: "mdi-thumb-up-outline",
  }
];

const MapRepositoryStatus = new Map(
  RepositoryStatus.map(key => [key.id, key])
);

const SelectRepositoryStatus = RepositoryStatus.map((x) => {
  return {
    value: x.id,
    text: x.label,
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
  MapRepositoryStatus,
  SelectRepositoryStatus,
  RepositoryPerPage,
};