import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;

public class Gradient {
    public static void main(String[] args) throws IOException {
        ArrayList<ArrayList<double[]>> points = new ArrayList<>();
        ArrayList<double[]> row = new ArrayList<>();
        double x, y, z, last = 0;

        try (BufferedReader reader = Files.newBufferedReader(Path.of("data/ncsutest.xyz"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                // Split line by spaces and read coordinates
                String[] tokens = line.split("\\s+");
                x = Double.parseDouble(tokens[0]);
                y = Double.parseDouble(tokens[1]);
                z = Double.parseDouble(tokens[2]);

                // If y value has changed, add the entire row to the list and restart
                if (y != last) {
                    if (row.size() != 0) {
                        points.add(row);
                    }
                    row = new ArrayList<>();
                }
                
                // Add points
                row.add(new double[] {x, y, z});
                last = y;
            }
            points.add(row);
        }
    }
}