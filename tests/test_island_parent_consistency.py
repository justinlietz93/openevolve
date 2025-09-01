"""
Test for island parent-child consistency - Programs' parents should be in the corresponding islands
"""

import unittest
from openevolve.config import Config
from openevolve.database import ProgramDatabase, Program


class TestIslandParentConsistency(unittest.TestCase):
    """Test that parent-child relationships respect island boundaries"""

    def test_parent_child_island_consistency(self):
        """Test that children are added to the same island as their parents"""
        config = Config()
        config.database.num_islands = 3
        database = ProgramDatabase(config.database)

        # Create initial program on island 0
        initial_program = Program(
            id="initial", code="def initial(): pass", metrics={"score": 0.5}, iteration_found=0
        )
        database.add(initial_program)  # Should go to island 0 (current_island)

        # Verify initial program is on island 0
        self.assertIn("initial", database.islands[0])
        self.assertEqual(initial_program.metadata.get("island"), 0)

        # Now switch to island 1
        database.next_island()
        self.assertEqual(database.current_island, 1)

        # Create a child of the initial program
        child_program = Program(
            id="child1",
            code="def child1(): pass",
            parent_id="initial",  # Parent is on island 0
            metrics={"score": 0.6},
            iteration_found=1,
        )

        # Add child without specifying target_island
        # This is what happens in process_parallel.py line 445
        database.add(child_program)

        # With the fix: child should go to parent's island (0), not current_island (1)
        parent_island = database.programs["initial"].metadata.get("island", 0)
        child_island = database.programs["child1"].metadata.get("island")

        # Check if parent is in child's island (this is what the user's assertion checks)
        if child_program.parent_id:
            # This is the exact check from the issue report - should now pass
            self.assertIn(
                child_program.parent_id,
                database.islands[child_island],
                "Parent should be in child's island",
            )

        # Verify child is on same island as parent
        self.assertEqual(
            parent_island,
            child_island,
            f"Child should be on same island as parent. Parent: island {parent_island}, Child: island {child_island}",
        )

    def test_multiple_generations_island_drift(self):
        """Test that island drift happens across multiple generations"""
        config = Config()
        config.database.num_islands = 4
        database = ProgramDatabase(config.database)

        # Create a lineage
        programs = []
        for i in range(10):
            if i == 0:
                # Initial program
                prog = Program(
                    id=f"prog_{i}",
                    code=f"def prog_{i}(): pass",
                    metrics={"score": 0.1 * i},
                    iteration_found=i,
                )
            else:
                # Child of previous
                prog = Program(
                    id=f"prog_{i}",
                    code=f"def prog_{i}(): pass",
                    parent_id=f"prog_{i-1}",
                    metrics={"score": 0.1 * i},
                    iteration_found=i,
                )

            database.add(prog)
            programs.append(prog)

            # Switch islands periodically (simulating what happens in evolution)
            if i % 3 == 0:
                database.next_island()

        # Check island consistency
        inconsistent_pairs = []
        for prog in programs:
            if prog.parent_id:
                parent = database.programs.get(prog.parent_id)
                if parent:
                    parent_island = parent.metadata.get("island")
                    child_island = prog.metadata.get("island")

                    # Check if parent is in child's island
                    if prog.parent_id not in database.islands[child_island]:
                        inconsistent_pairs.append((prog.parent_id, prog.id))

        # With the fix, we should find NO inconsistent parent-child island assignments
        self.assertEqual(
            len(inconsistent_pairs),
            0,
            f"Found {len(inconsistent_pairs)} inconsistent parent-child pairs: {inconsistent_pairs}",
        )

        # Verify all parent-child pairs are on the same island
        for prog in programs:
            if prog.parent_id:
                parent = database.programs.get(prog.parent_id)
                if parent:
                    parent_island = parent.metadata.get("island")
                    child_island = prog.metadata.get("island")
                    self.assertEqual(
                        parent_island,
                        child_island,
                        f"Parent {prog.parent_id} (island {parent_island}) and "
                        f"child {prog.id} (island {child_island}) should be on same island",
                    )

    def test_explicit_migration_override(self):
        """Test that explicit target_island overrides parent island inheritance"""
        config = Config()
        config.database.num_islands = 3
        database = ProgramDatabase(config.database)

        # Create parent on island 0
        parent = Program(
            id="parent", code="def parent(): pass", metrics={"score": 0.5}, iteration_found=0
        )
        database.add(parent)  # Goes to island 0
        self.assertIn("parent", database.islands[0])

        # Create child but explicitly send to island 2 (migration)
        migrant_child = Program(
            id="migrant",
            code="def migrant(): pass",
            parent_id="parent",
            metrics={"score": 0.7},
            iteration_found=1,
        )
        database.add(migrant_child, target_island=2)  # Explicit migration

        # Verify migrant went to island 2, not parent's island 0
        self.assertIn("migrant", database.islands[2])
        self.assertNotIn("migrant", database.islands[0])
        self.assertEqual(migrant_child.metadata.get("island"), 2)

        # Parent should still be on island 0
        self.assertEqual(database.programs["parent"].metadata.get("island"), 0)


if __name__ == "__main__":
    unittest.main()
