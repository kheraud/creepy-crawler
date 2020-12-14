import { status as repoStatus } from "../../app.config"

const MapRepositoryStatus = new Map(
  repoStatus.map(key => [key.id, key])
);

const SelectRepositoryStatus = repoStatus.map((x) => {
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

export {
  SelectRepositorySort,
  MapRepositoryStatus,
  SelectRepositoryStatus,
};