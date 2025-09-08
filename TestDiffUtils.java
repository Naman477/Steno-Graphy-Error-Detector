import com.github.difflib.DiffUtils;
import com.github.difflib.patch.Patch;
import com.github.difflib.patch.AbstractDelta;
import com.github.difflib.patch.DeltaType;

import java.util.Arrays;
import java.util.List;

public class TestDiffUtils {
    public static void main(String[] args) {
        List<String> source = Arrays.asList("This", "is", "a", "test.");
        List<String> target = Arrays.asList("This", "is", "a", "test.");

        Patch<String> patch = DiffUtils.diff(source, target);

        System.out.println("Patch deltas empty: " + patch.getDeltas().isEmpty());
        System.out.println("Number of deltas: " + patch.getDeltas().size());

        if (!patch.getDeltas().isEmpty()) {
            for (AbstractDelta<String> delta : patch.getDeltas()) {
                System.out.println("Delta Type: " + delta.getType());
                System.out.println("Source Lines: " + delta.getSource().getLines());
                System.out.println("Target Lines: " + delta.getTarget().getLines());
            }
        }
    }
}